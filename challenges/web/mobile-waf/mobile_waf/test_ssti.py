import re

def is_ssti_inner(m_text):
    m_text = m_text.strip()
    # If it is only a single simple variable name (letters and underscores), it's benign template var
    if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', m_text):
        # Unless it is a known dangerous template global like config, self, request
        if m_text.lower() in ['config', 'self', 'request', 'lipsum', 'cycler', 'joiner', 'namespace']:
            return True
        return False
    return True

print("customer_name:", is_ssti_inner("customer_name"))
print("tracking_code:", is_ssti_inner("tracking_code"))
print("ship_date:", is_ssti_inner("ship_date"))
print("7*7:", is_ssti_inner("7*7"))
print("cycler.__init__:", is_ssti_inner("cycler.__init__"))
print("config:", is_ssti_inner("config"))
print("os.popen('id').read():", is_ssti_inner("os.popen('id').read()"))
