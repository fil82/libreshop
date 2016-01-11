import importlib
import logging
import braintree
from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.views.generic import FormView, TemplateView
from ipware.ip import get_real_ip
from addresses.forms import AddressForm
from carts import SessionList
from products.models import Variant
from .forms import PaymentForm

# Set a universally unique identifier (UUID).
UUID = '9bf75036-ec58-4188-be12-4f983cac7e55'

# Initialize logger.
logger = logging.getLogger(__name__)


def calculate_shipping_cost(*args, **kwargs):

    results = []
    for api_name in settings.SHIPPING_APIS:
        index = api_name.rfind('.')
        module_name, attribute_name = api_name[:index], api_name[index+1:]
        module, function = None, None
        try:
            module = importlib.import_module(module_name)
            function = getattr(module, attribute_name)
        except ImportError as e:
            logger.critical('Unable to import module \'%s\'.' % module_name)
        except AttributeError as e:
            logger.critical('\'%s\' module has no attribute \'%s\'.' %
                (module_name, attribute_name))
        else:
            logger.info('Calling \'%s.%s\'...' % (module_name, attribute_name))
            result = function(*args, **kwargs)
            logger.info('Called \'%s.%s\'.' % (module_name, attribute_name))
            results.append(result)

    return Decimal(results[0]).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP) if results else None

# Create views here.
class ConfirmationView(TemplateView):

    template_name = 'orders/confirmation.html'


class CheckoutFormView(FormView):

    form_class = AddressForm
    template_name = 'orders/checkout.html'
    success_url = '/'

    def __init__(self, *args, **kwargs):
        super(CheckoutFormView, self).__init__(*args, **kwargs)

        self.client_token = braintree.ClientToken.generate()


    def post(self, request, *args, **kwargs):

        template_response = None
        if not self.session_data_is_valid():
            session_data = self.request.session[UUID]

            previous_index = self.steps.index(self.current_step)-1
            previous_step_key = self.steps[previous_index]['name']

            malformed_data = session_data.get(previous_step_key, None)

            if previous_step_key in session_data:
                del session_data[previous_step_key]
                self.request.session.modified = True

            self.current_step = self.get_current_step()

            form_class = self.get_form_class()
            form = form_class(data=malformed_data)

            if not form.is_valid():
                form.add_error(None, 'Something went wrong here...')

            template_names = self.get_template_names()
            context_data = self.get_context_data(form=form)

            template_response = TemplateResponse(
                request, template_names, context_data
            )

        return (
            super(CheckoutFormView, self).post(request, *args, **kwargs)
            if not template_response else template_response
        )


    def dispatch(self, request, *args, **kwargs):

        if not self.request.session.has_key(UUID):
            self.request.session[UUID] = {}

        session_cart = SessionList(self.request.session)
        self.cart = [
            variant for pk in session_cart
            for variant in Variant.objects.filter(pk=pk)
        ]
        self.subtotal = sum(variant.price for variant in self.cart)

        self.shipping_address = self.request.session[UUID].get('shipping')
        self.shipping_cost = None

        if self.shipping_address:
            products = {
                'id': 'anvil-fashion-fit-t-shirt',
                'color': 'Green Apple',
                'size': 'lrg',
                'quantity': len(self.cart)
            }
            self.shipping_cost = calculate_shipping_cost(
                address=self.shipping_address,
                products=products
            )

        print(type(self.shipping_cost), type(self.subtotal))

        self.steps = (
            {
                'name': 'shipping',
                'form_class': AddressForm,
                'template': 'orders/checkout.html',
                'context': {
                    'description': 'where are we sending this?',
                }
            },
            {
                'name': 'payment',
                'form_class': PaymentForm,
                'template': 'orders/checkout.html',
                'form_kwargs': {
                    'amount': (
                        (self.subtotal + self.shipping_cost)
                        if self.shipping_cost else 0.00
                    )
                },
                'context': {
                    'description': 'how are you paying?',
                    'client_token': self.client_token,
                    'shipping_cost': self.shipping_cost,
                    'total': (
                        (self.subtotal + self.shipping_cost)
                        if self.shipping_cost else 0.00
                    )
                }
            },
        )

        self.current_step = self.get_current_step()

        return super(CheckoutFormView, self).dispatch(request, *args, **kwargs)


    def get_current_step(self):
        '''
        Get the current step within the form wizard.
        '''
        completed_steps = self.request.session.get(UUID, {})

        remaining_steps = [
            step for step in self.steps if step['name'] not in completed_steps
        ]
        current_step = remaining_steps[0] if remaining_steps else None

        logger.debug('Completed steps: %s' % ', '.join(step for step in completed_steps))
        logger.debug('Remaining steps: %s' % ', '.join(step['name'] for step in remaining_steps))
        logger.debug('Current step: %s' % (current_step['name'] if current_step else ''))

        return current_step


    def get_template_names(self):
        template_name = self.current_step['template']

        return [template_name]


    def get_form_class(self):
        logger.debug('Getting form class...')
        return self.current_step['form_class']


    def get_form_kwargs(self):
        kwargs = super(CheckoutFormView, self).get_form_kwargs()

        if 'form_kwargs' in self.current_step:
            kwargs.update(self.current_step['form_kwargs'])

        return kwargs


    def get_form(self, form_class=None):
        '''
        Get the Form object that will be supplied to the FormView's context.
        '''
        # Instantiate Form.
        form = super(CheckoutFormView, self).get_form(form_class=form_class)

        if isinstance(form, AddressForm):
            # Determine the IP address associated to the HTTP Request.
            ip_address = get_real_ip(self.request)
    
            # Populate the form's `country` field with the user's apparent
            # location.
            if ip_address and not form.is_bound:
                geo_ip2 = GeoIP2()
                location = geo_ip2.country(ip_address)
                form.fields['country'].initial = location['country_code']

        logger.debug(
            'Got %s %s form' % (
                'bound' if form.is_bound else 'unbound', form.__class__.__name__
            )
        )

        return form


    def form_valid(self, form):

        self.request.session[UUID].update({
            self.current_step['name']: form.cleaned_data,
        })
        self.request.session.modified = True

        return super(CheckoutFormView, self).form_valid(form)


    def session_data_is_valid(self):

        session_data = self.request.session.get(UUID, None)

        is_valid = True
        if session_data:
            completed_steps = [
                step for step in self.steps if step['name'] in session_data
            ]

            for completed_step in completed_steps:
                step_name = completed_step['name']
                form_class = completed_step['form_class']

                form = form_class(data=session_data[step_name])
                if not form.is_valid():
                    is_valid = False
                    break

        return is_valid


    def get_success_url(self):
        logger.info('Getting Success URL...')

        if self.get_current_step():
            url = reverse('checkout:main')
        else:
            url = reverse('checkout:confirmation')
            del self.request.session[UUID]

        logger.info('Redirecting to %s' % url)

        return url


    def get_context_data(self, **kwargs):
        context = super(CheckoutFormView, self).get_context_data(**kwargs)

        current_position = next(
            i for (i, step) in enumerate(self.steps)
            if step['name'] == self.current_step['name']
        )

        context.update({
            'cart': self.cart,
            'subtotal': self.subtotal,
            'current_position': current_position,
            'steps': enumerate(self.steps),
        })

        step_context = self.current_step['context']
        if step_context:
            context.update(step_context)

        return context
