DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'brandpulsarprimarydb',
        'USER': 'brandpulsarprimaryuser',
        'PASSWORD': 'icui4cu',
        'HOST': 'localhost',
        'PORT': 5432
    }
}

STRIPE_SECRET_KEY = "sk_test_CPDJaW3ubEBaR50ggcvwnXZ400XxjfAcvs"
STRIPE_PUBLISHABLE_KEY = "pk_test_wmAGRMcQtiJ2u8pPr3Adg2mv00e7iErr6z"

STRIPE_INSTALMENT_WEBHOOK_ENPOINT_SECRET = 'whsec_QXop9bZRnUQsLZAeu3PcybDICFuqiJKw'
STRIPE_FEATURED_WEBHOOK_ENPOINT_SECRET = 'whsec_as9fTEjKmuVEA0V9B0SqnRWR8nsNQ30N'

BASE_URL = 'http://127.0.0.1:8000'
