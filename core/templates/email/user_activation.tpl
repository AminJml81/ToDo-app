{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello {{ user_email }}
{% endblock %}

{% block html %}
<h3>click the link below to activate your account</h3>
<h2>http://127.0.0.1:8000/accounts/api/v1/activation/confirm/{{token}}/<h2>
{% endblock %}