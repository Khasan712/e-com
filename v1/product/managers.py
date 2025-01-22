from django.contrib.auth.base_user import BaseUserManager
from uuid import uuid4


class BarcodeCustomManager(BaseUserManager):
    def generate_barcode(self):
        new_barocde = uuid4().int % 1000000000
        barcode = self.model(
            code=new_barocde,
            title="System generated",
        )
        barcode.save(using=self._db)
        return barcode
