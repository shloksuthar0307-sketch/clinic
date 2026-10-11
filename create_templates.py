import os

base_dir = r'd:\hospital\templates\accounts'

html_base = """{% extends 'base.html' %}
{% load widget_tweaks %}

{% block body %}
<div class="min-h-screen flex relative overflow-hidden bg-white dark:bg-darkbg">
    <!-- Abstract background shape -->
    <div class="absolute inset-0 z-0 overflow-hidden pointer-events-none">
        <div class="absolute -top-40 -right-40 w-96 h-96 bg-primary/10 rounded-full blur-3xl"></div>
        <div class="absolute top-40 -left-40 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl"></div>
    </div>

    <div class="flex-1 flex flex-col justify-center py-12 px-4 sm:px-6 lg:flex-none lg:px-20 xl:px-24 z-10 w-full lg:w-1/2">
        <div class="mx-auto w-full max-w-sm lg:w-96 fade-in">
            <div>
                <a href="{% url 'root' %}" class="flex items-center gap-2 font-bold text-2xl text-primary">
                    <i data-lucide="activity" class="h-8 w-8"></i>
                    <span>Pulse<span class="text-gray-900 dark:text-white">Med</span></span>
                </a>
                <h2 class="mt-8 text-3xl font-extrabold text-gray-900 dark:text-white tracking-tight">{TITLE}</h2>
                <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
                    {SUBTITLE}
                </p>
            </div>

            <div class="mt-8 slide-up">
                {CONTENT}
            </div>
        </div>
    </div>
    
    <!-- Hero Image side -->
    <div class="hidden lg:block relative w-1/2 bg-gray-50 dark:bg-darkcard border-l border-gray-200 dark:border-gray-800">
        <div class="absolute inset-0 flex flex-col justify-center p-12">
            <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-6">The Next-Generation Operating System for Doctors.</h1>
            <p class="text-lg text-gray-600 dark:text-gray-400 mb-8 max-w-lg">Manage patients, streamline prescriptions, and analyze your revenue all in one beautiful, lightning-fast interface.</p>
        </div>
    </div>
</div>
{% endblock %}
"""

# 1. password_reset.html
content1 = """<form method="POST" class="space-y-6">
    {% csrf_token %}
    {% if form.non_field_errors %}
    <div class="bg-red-50 text-red-600 p-3 rounded-lg text-sm border border-red-100 flex items-start gap-2">
        <span>{{ form.non_field_errors.0 }}</span>
    </div>
    {% endif %}
    
    <div>
        <label for="id_email" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Email address</label>
        <div class="mt-1 relative">
            {% render_field form.email class="appearance-none block w-full px-3 py-2.5 border border-gray-300 dark:border-gray-700 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-white transition-all" %}
        </div>
    </div>

    <div>
        <button type="submit" class="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-xl shadow-sm text-sm font-medium text-white bg-primary hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all">
            Send Reset Link
        </button>
    </div>
</form>"""

with open(os.path.join(base_dir, 'password_reset.html'), 'w') as f:
    f.write(html_base.replace('{TITLE}', 'Reset your password').replace('{SUBTITLE}', 'Remember your password? <a href="{% url \'login\' %}" class="font-medium text-primary hover:text-indigo-500">Sign in</a>').replace('{CONTENT}', content1))


# 2. password_reset_done.html
content2 = """<div class="bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400 p-4 rounded-xl border border-green-100 dark:border-green-900/50">
    <p>We've emailed you instructions for setting your password, if an account exists with the email you entered. You should receive them shortly.</p>
    <p class="mt-4">If you don't receive an email, please make sure you've entered the address you registered with, and check your spam folder.</p>
</div>
<div class="mt-6">
    <a href="{% url 'login' %}" class="w-full flex justify-center py-2.5 px-4 border border-gray-300 dark:border-gray-600 rounded-xl shadow-sm text-sm font-medium text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-800 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all">
        Return to sign in
    </a>
</div>"""

with open(os.path.join(base_dir, 'password_reset_done.html'), 'w') as f:
    f.write(html_base.replace('{TITLE}', 'Check your email').replace('{SUBTITLE}', 'We have sent you a reset link.').replace('{CONTENT}', content2))


# 3. password_reset_confirm.html
content3 = """{% if validlink %}
<form method="POST" class="space-y-6">
    {% csrf_token %}
    {% if form.non_field_errors %}
    <div class="bg-red-50 text-red-600 p-3 rounded-lg text-sm border border-red-100 flex items-start gap-2">
        <span>{{ form.non_field_errors.0 }}</span>
    </div>
    {% endif %}
    
    {% for field in form %}
    <div>
        <label for="{{ field.id_for_label }}" class="block text-sm font-medium text-gray-700 dark:text-gray-300">{{ field.label }}</label>
        <div class="mt-1 relative">
            {% render_field field class="appearance-none block w-full px-3 py-2.5 border border-gray-300 dark:border-gray-700 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-white transition-all" %}
            {% if field.errors %}
            <p class="text-red-500 text-xs mt-1">{{ field.errors.0 }}</p>
            {% endif %}
        </div>
    </div>
    {% endfor %}

    <div>
        <button type="submit" class="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-xl shadow-sm text-sm font-medium text-white bg-primary hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all">
            Change Password
        </button>
    </div>
</form>
{% else %}
<div class="bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 p-4 rounded-xl border border-red-100 dark:border-red-900/50">
    <p>The password reset link was invalid, possibly because it has already been used. Please request a new password reset.</p>
</div>
<div class="mt-6">
    <a href="{% url 'password_reset' %}" class="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-xl shadow-sm text-sm font-medium text-white bg-primary hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all">
        Request new link
    </a>
</div>
{% endif %}"""

with open(os.path.join(base_dir, 'password_reset_confirm.html'), 'w') as f:
    f.write(html_base.replace('{TITLE}', 'Set new password').replace('{SUBTITLE}', 'Please enter your new password twice so we can verify you typed it in correctly.').replace('{CONTENT}', content3))


# 4. password_reset_complete.html
content4 = """<div class="bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400 p-4 rounded-xl border border-green-100 dark:border-green-900/50">
    <p>Your password has been set. You may go ahead and sign in now.</p>
</div>
<div class="mt-6">
    <a href="{% url 'login' %}" class="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-xl shadow-sm text-sm font-medium text-white bg-primary hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all">
        Sign in
    </a>
</div>"""

with open(os.path.join(base_dir, 'password_reset_complete.html'), 'w') as f:
    f.write(html_base.replace('{TITLE}', 'Password reset complete').replace('{SUBTITLE}', 'Your password has been successfully reset.').replace('{CONTENT}', content4))

print("Templates created successfully.")
