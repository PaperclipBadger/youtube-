from datetime import datetime

with open('templates/template.opml', 'r') as f:
    OPML_TEMPLATE = f.read()
with open('templates/folder.opml', 'r') as f:
    FOLDER_TEMPLATE = f.read()
with open('templates/subscription.opml', 'r') as f:
    SUBSCRIPTION_TEMPLATE = f.read()

class OPMLBuilder():
    """Builds a subscriptions OPML."""

    def __init__(self, folder_name=None):
        if folder_name:
            self.name = folder_name
        self.folders = []
        self.subscriptions = []

    def addFolder(self, folder_name):
        if [f for f in self.folders if f.name == folder_name]:
            raise ValueError('There is already a folder with that name.')
        self.folders.append(Folder(folder_name))

    def addSubscription(self, name, guid):
        self.subscriptions.append(Subscription(name, guid))

    def __getitem__(self, key):
        result = [f for f in self.folders if f.name == key]
        if not result:
            raise ValueError('No folder with that name.')
        return result[0]
    
    def __delitem__(self, key):
        result = [f for f in self.folders if f.name == key]
        if not result:
            raise ValueError('No folder with that name.')
        del result[0]

    def __str__(self):
        now = str(datetime.utcnow())
        if self.folders:
            folders = '\n'.join(str(f) for f in self.folders)
        else:
            folders = ''
        subscriptions = '\n'.join(str(s) for s in self.subscriptions)
        return OPML_TEMPLATE.format(
                time=now,
                folders=folders,
                subscriptions=subscriptions
                )


class Folder(OPMLBuilder):
    def __str__(self):
        if self.folders:
            folders = '\n'.join(str(f) for f in self.folders)
        else:
            folders = ''
        subscriptions = '\n'.join(str(s) for s in self.subscriptions)
        return FOLDER_TEMPLATE.format(
                name=self.name, 
                folders=folders,
                subscriptions=subscriptions
                )


class Subscription():
    def __init__(self, name, guid):
        self.name = name
        self.guid = guid

    def __repr__(self):
        return '{!s}({!r}, {!r})'.format(self.__class__, self.name, self.guid)

    def __str__(self):
        return SUBSCRIPTION_TEMPLATE.format(name=self.name.encode('utf-8'), guid=self.guid)



