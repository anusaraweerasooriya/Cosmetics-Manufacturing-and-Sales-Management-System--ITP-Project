from django import forms
from django.forms import Textarea
from .models import Product, WarehouseRequest, RawMaterial, Equipment, Packaging, WarehouseEmployee


class ProductUpdateForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [
            'quantity',
            'reorderLevel',
        ]

        labels = {
            "quantity": "In Stock",
            "reorderLevel": "Reorder Level",
        }


class WarehouseRequestForm(forms.ModelForm):

    class Meta:
        model = WarehouseRequest
        fields = [
            'request_ID',
            'itemName',
            'quantity',
            'req_from',
            'type',
            'due_Date',
        ]

        labels = {
            "request_ID": "Request ID",
            "req_from": "Request From",
            "due_Date": "Due Date",
            "itemName": "Item Name",
        }

        widgets = {
            'due_Date': forms.DateInput(attrs={'type': 'date', 'style': 'cursor: pointer'}),
        }


class RawMaterialForm(forms.ModelForm):

    class Meta:
        model = RawMaterial
        fields = [
            'itemID',
            'itemName',
            'category',
            'quantity',
            'description',
            'reorderLevel',
            'expireDate',
            'receivedDate',
        ]

        labels = {
            'itemID': 'Item ID',
            'itemName': 'Item Name',
            'reorderLevel': 'Reorder Level',
            'expireDate': 'Expire Date',
            'receivedDate': 'Receive Date',
        }

        widgets = {
            'description': Textarea(attrs={'rows': 3}),
            'expireDate': forms.DateInput(attrs={'type': 'date', 'style': 'cursor: pointer'}),
            'receivedDate': forms.DateInput(attrs={'type': 'date', 'style': 'cursor: pointer'}),
        }

    def clean(self):
        cleaned_data = super(RawMaterialForm, self).clean()
        itemid = cleaned_data.get("itemID")
        if itemid:
            if len(itemid) < 7:
                msg = "ID should be 7 characters long"
                self.add_error('itemID', msg)


class EquipmentForm(forms.ModelForm):

    class Meta:
        model = Equipment
        fields = [
            'itemID',
            'itemName',
            'category',
            'quantity',
            'description',
            'status',
            'lastMaintenanceDate',
            'nextMaintenanceDate',
        ]

        labels = {
            'itemID': 'Item ID',
            'itemName': 'Item Name',
            'lastMaintenanceDate': 'Last Maintenance',
            'nextMaintenanceDate': 'Next Maintenance',
            'status': 'Condition',

        }

        widgets = {
            'description': Textarea(attrs={'rows': 3}),
            'lastMaintenanceDate': forms.DateInput(attrs={'type': 'date', 'style': 'cursor: pointer'}),
            'nextMaintenanceDate': forms.DateInput(attrs={'type': 'date', 'style': 'cursor: pointer'}),
        }

    def clean(self):
        cleaned_data = super(EquipmentForm, self).clean()
        last = cleaned_data.get("lastMaintenanceDate")
        nextmaintain = cleaned_data.get("nextMaintenanceDate")
        if last and nextmaintain:
            if last > nextmaintain:
                msg = "Next Maintain Date Should be Greater"
                self.add_error('nextMaintenanceDate', msg)


class PackagingForm(forms.ModelForm):

    class Meta:
        model = Packaging
        fields = [
            'itemID',
            'itemName',
            'category',
            'quantity',
            'description',
            'reorderLevel',
            'materialType'
        ]

        labels = {
            'itemID': 'Item ID',
            'itemName': 'Item Name',
            'reorderLevel': 'Reorder Level',
            'materialType': 'Material Type',
        }

        widgets = {
            'description': Textarea(attrs={'rows': 3}),
        }


class AcceptEmployeeForm(forms.ModelForm):
    class Meta:
        model = WarehouseEmployee
        fields = [
            'employee',
            'workingArea',
        ]

        labels = {
            'workingArea': 'Sector',
        }


class BatchAcceptForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product',
            'quantity',
            'reorderLevel',
        ]
        labels = {
            'reorderLevel': 'Re-Order Level'
        }
