from imapclient import IMAPClient

from trainer import Trainer


def get_imap_variable(name):
    if name in os.environ:
        return os.environ[name]
    
    with open('.envrc', 'r') as f:
        for line in f:
            if line.startswith(f'export {name}='):
                return line.split('=')[1].strip().strip('"')

def get_imap_host():
    return get_imap_variable('IMAP_HOST')

def get_imap_port():
    return int(get_imap_variable('IMAP_PORT'))

def get_imap_username():
    return get_imap_variable('IMAP_USERNAME')

def get_imap_password():
    return get_imap_variable('IMAP_PASSWORD')



model_trainer = Trainer()

imap_host = get_imap_host()
imap_port = get_imap_port()
imap_username = get_imap_username()
imap_password = get_imap_password()

with IMAPClient(host=get_imap_host(), port=get_imap_port(), ssl=False) as client:
    client.login(get_imap_username(), get_imap_password())

    folder = 'Folders/Bad Truth'
    select_info = client.select_folder(folder)
    print(f"{select_info[b'EXISTS']} messages in {folder}")
    
    messages = client.search('ALL')

    for msgid, data in client.fetch(messages, ['RFC822']).items():
        rfc822 = data[b'RFC822']
        print(f'Counting ID #{msgid}...')
        model_trainer.update_counts(rfc822.decode(), is_good=False)

    print(model_trainer.model.num_bad_emails)
    print(model_trainer.model.bad_counts)
