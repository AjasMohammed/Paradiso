class ShopRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'shop':
            return 'secondary'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'shop':
            return 'secondary'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        # Decide if a relation between two objects is allowed
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Decide if migration is allowed for a database
        return True
