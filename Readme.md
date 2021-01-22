# Brandpulsar

## Site Address
http(s): ***brandpulsar.com***

ipv4: ***157.230.19.185***

## Versions

    python v3.7

    django v3.0.5


## Prerequisites

`pip install -r requirements.txt`

**Database**: `brandpulsar.settings.DATABASES['default']`

## Assets

>Static
>
>> path: **/static**
`./manage.py collectstatic`
>
>Media
>
>> path: **/media-root**


## Migrations

>Create New
`./manage.py makemigrations`

>Deploy Existing
`./manage.py migrate`

## Logs (production only)

>Application logs

    log/gunicorn.log

>Server logs

    log/brandpulsar.nginx.{event}.log

