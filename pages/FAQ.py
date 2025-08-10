import streamlit as st

aqs = {
    "What is Mahaconnect (Internet Banking)?": 
        "• Mahaconnect is Bank of Maharashtra’s secure Internet Banking platform.\n"
        "• Provides 24×7 account access from anywhere.\n"
        "• Allows balance enquiry and account statement download.\n"
        "• Enables fund transfers within BOM and to other banks (NEFT/RTGS/IMPS).\n"
        "• Supports utility bill payments (electricity, water, gas, etc.).\n"
        "• Supports mobile and DTH recharges.\n"
        "• Ensures secure transactions with 128-bit SSL encryption and multi-factor authentication.",

    "Who can use Mahaconnect?": 
        "• Any customer with an account at a Core Banking Solution (CBS) branch.\n"
        "• Customers at non-CBS branches must transfer to a CBS branch to use the service.\n"
        "• Available for savings, current, and select deposit accounts.",

    "How do I register for Internet Banking?": 
        "• Visit your nearest Bank of Maharashtra branch.\n"
        "• Fill in the Internet Banking application form (available at the branch or online).\n"
        "• Submit the form along with a valid photo ID proof.\n"
        "• The bank will process your request and send your User ID and Password to your registered address.",

    "Forgot Password or User ID?": 
        "• Use the 'Forgot Password/User ID' option on the Mahaconnect login page.\n"
        "• Alternatively, contact the Internet Banking Helpdesk.\n"
        "• Keep your account details and registered mobile/email handy for verification.",

    "Is it safe to login from a cyber café?": 
        "• Avoid public computers where possible.\n"
        "• If unavoidable:\n"
        "   - Do not save your password.\n"
        "   - Ensure you log out properly after use.\n"
        "   - Avoid downloading/saving account statements on public machines.",

    "What is MahaSecure?": 
        "• A desktop and mobile security application from BOM.\n"
        "• Ensures encrypted banking sessions.\n"
        "• Adds security via OTP, MPIN, and secret questions.\n"
        "• Prevents phishing and keylogging attacks.",

    "How do I activate MahaSecure on a new device?": 
        "• Install the MahaSecure application from BOM’s official website.\n"
        "• Enter your User ID and OTP sent to your registered mobile number.\n"
        "• Answer the secret question you set earlier.\n"
        "• Set a 4-digit MPIN for quick future logins.",

    "Why doesn't the virtual keyboard appear?": 
        "• Ensure JavaScript (Active Scripting) is enabled in your browser settings.\n"
        "• Refresh the page or restart the browser.\n"
        "• Check if you’re using an updated version of your browser.",

    "What bills can I pay online?": 
        "• Utility bills – electricity, water, gas.\n"
        "• Telephone bills – landline and mobile.\n"
        "• DTH recharges.\n"
        "• Insurance premium payments.\n"
        "• Credit card bills.\n"
        "• Taxes and government payments.",

    "Who can avail utility bill payment services?": 
        "• All registered Internet Banking customers.\n"
        "• Service is available free of charge.\n"
        "• Requires only a valid account and login credentials.",

    "How do I get support?": 
        "• Call toll-free: 1800-233-4526 / 1800-102-2636.\n"
        "• Email: mahaconnect@mahabank.co.in or mahasecure@mahabank.co.in.\n"
        "• Visit your nearest branch for assistance."
}


for q, a in aqs.items():

    with st.expander(q):
        st.write(a)
