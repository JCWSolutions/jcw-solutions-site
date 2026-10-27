# Single source of truth for details that appear on several pages.
# Anything wrapped in todo() renders as a highlighted [TO CONFIRM] marker
# and the build refuses to produce a "release" build while any remain.

def todo(text):
    return f'<mark class="todo">[TO CONFIRM: {text}]</mark>'

SITE_URL = "https://jcw.solutions"
BRAND = "JCW Solutions"

# Legal entity behind the site and apps (Ltd name + number + registered office if a company)
LEGAL_ENTITY = "JCW Digital Ltd"
COMPANY_DETAILS = "Registered in England and Wales, company number 17532846. Registered office: 6 Cornwallis Grove, London N9 0JS."

CONTACT_EMAIL = '<a href="mailto:josh@jcw.solutions">josh@jcw.solutions</a>'
SUPPORT_EMAIL = '<a href="mailto:josh@jcw.solutions">josh@jcw.solutions</a>'
PRIVACY_EMAIL = '<a href="mailto:josh@jcw.solutions">josh@jcw.solutions</a>'

POLICY_EFFECTIVE = "27 October 2026"

# Page-specific facts referenced as {{todo_KEY}}. Replace a value with plain
# confirmed text (no todo()) once it is decided.
FACTS = {
    "DIAGNOSTICS": "Aggregated, anonymous usage and crash statistics provided by Apple, only if you have chosen to share analytics with app developers in iOS Settings. Freeday contains no third-party analytics or crash-reporting tools.",
    "DIAGNOSTICS_SOURCE": "Apple, with your consent",
    "ACCOUNT": "Freeday does not currently require an account. If we introduce optional accounts, we will update this policy and tell you in the app first.",
    "WALLET_OFFDEVICE": "Wallet data is never sent off your device: not to our server and not to any service provider. It is excluded from the goal assistant described in section 5.",
    "AI_FEATURE": "Freeday's goal assistant lets you ask questions about your financial goals. To answer, the app sends your question and the related transactions to an AI model that we run ourselves, on our own server in the UK, using the open-source Ollama software. No third-party AI company receives your data. The goal assistant is optional.",
    "AI_DATA": "Your question and the transactions used to answer it (description, amount, date and category) from records you have entered or imported.",
    "AI_WALLET": "No. Data from Apple Wallet is never sent.",
    "AI_PROVIDER": "JCW Solutions, on its own server. No third-party AI provider is involved.",
    "AI_LOCATION": "United Kingdom",
    "AI_RETENTION": "Kept on our server for up to 24 hours to provide the answer, then deleted.",
    "AI_TRAINING": "No. The model runs on our own server and is not trained on your data.",
    "AI_OPTOUT": "Yes. The goal assistant is optional and can be turned off in the app.",
    "AI_TRANSIT": "sent over an encrypted (HTTPS/TLS) connection.",
    "PROCESSORS": "We do not use a third-party AI provider; the goal assistant runs on our own server (section 5). Support emails are handled by our email hosting provider.",
    "TRANSFERS": "Freeday data that we process ourselves (section 5) stays in the UK. Data in your iCloud account is handled by Apple under its own terms.",
    "SUPPORT_RETENTION": "up to 12 months after your enquiry is resolved",
    "SUPPORT_RESPONSE": "3 working days",
    "HOST": "GitHub Pages, provided by GitHub, Inc.",
    "ENQUIRY_RETENTION": "12 months",
    "INAPP_DELETE": "with Settings → Delete all my data",
    "CHILDREN": "Freeday is intended for people aged 18 and over and is not directed at children.",
}
