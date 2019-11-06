from django.shortcuts import render
import uuid
import datetime
from googleads import adwords
from googleads import oauth2
import google.oauth2.credentials
import google_auth_oauthlib.flow
# Create your views here.

CLIENT_ID = '254893498378-j9ba21uate11n0lmo44eigd9apgcl5br.apps.googleusercontent.com'
CLIENT_SECRET = 'p5EeYlyRNjGagOyCWpyT4Kyy'
REFRESH_TOKEN = '4/swH5rrCaEXYPxLMK8ZjfQ12341BiDmhNcy5xdbq9c44_TMiLWe96nFti3u1m2QvWiFTrXI-6QNMzKjC6GtvhHUQZ0S7Q'
DEVELOPER_TOKEN = 'iI7DnpGK-TZOOqG0at85YQ'
CLIENT_CUSTOMER_ID = '6187671662'


def add_campaign(adwords_client):
    campaign_service = adwords_client.GetService('CampaignService', version='v201809')
    budget_service = adwords_client.GetService('BudgetService', version='v201809')

    # Create a budget, which can be shared by multiple campaigns.
    budget = {
        'name': 'Interplanetary budget #%s' % uuid.uuid4(),
        'amount': {
            'microAmount': '50000000'
        },
        'deliveryMethod': 'STANDARD'
    }

    budget_operations = [{
        'operator': 'ADD',
        'operand': budget
    }]

    # Add the budget.
    budget_id = budget_service.mutate(budget_operations)['value'][0]['budgetId']
    context = {'budget_id': budget_id}
    return render('index.html', context)


def connect_api(request):
    oauth2_client = oauth2.GoogleRefreshTokenClient(
        CLIENT_ID,
        CLIENT_SECRET,
        REFRESH_TOKEN
    )
    adwords_client = adwords.AdWordsClient(
        DEVELOPER_TOKEN,
        oauth2_client,
        client_customer_id=CLIENT_CUSTOMER_ID
    )

    add_campaign(adwords_client)

    context = {
        'adwords_client': adwords_client
    }
    return render(request, 'index.html', context)


def get_token(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'C:\\client_secret.json',
        scopes=[oauth2.GetAPIScope('adwords')]
    )
    flow.redirect_uri = 'https://achedescontos.online/oauth2callback'

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    print(authorization_url, state)

    context = {
        'authorization_url': authorization_url
    }
    return render(request, 'index.html', context)


def oauth2callback(request):
    print(request)
