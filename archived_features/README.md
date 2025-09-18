# Archived Features

This folder contains all the features that have been archived from the Focus BJJ management system. These features are no longer in use but are preserved for potential future reference or restoration.

## Archived Features

### 1. Social Media Management
**Location:** `archived_features/social_media/`

**Components:**
- Templates:
  - `add_socialmedia.html` - Add new social media posts
  - `edit_socialmedia.html` - Edit existing posts
  - `delete_socialmedia.html` - Delete posts
- Static files:
  - `style_socialmedia.css` - Social media styling
- Models:
  - `Posts` - Social media posts model
- Views:
  - `SocialMedia` - List view for social media posts
  - `AddSocialMedia` - Create new posts
  - `UpdateSocialMedia` - Edit posts
  - `DeleteSocialMedia` - Delete posts
- Forms:
  - `SocialMediaForm` - Form for creating/editing posts

### 2. Product Management
**Location:** `archived_features/products/`

**Components:**
- Templates:
  - `add_product.html` - Add new products
  - `editarprodutos.html` - Edit products
  - `deletarprodutos.html` - Delete products
  - `products.html` - Product listing
- Models:
  - `ProductsList` - Product catalog model
  - `Product` - Individual product items in sales
- Views:
  - `AddProduct` - Create new products
  - `ProductList` - List all products
  - `EditProduct` - Edit products
  - `ProductDeleteView` - Delete products
- Forms:
  - `ProductForm` - Form for creating/editing products

### 3. Sales Management
**Location:** `archived_features/sales/`

**Components:**
- Templates:
  - `vendas.html` - Sales listing
  - `add_venda__.html` - Add new sales (in templates/archived_pages/)
  - `saledetails.html` - Sale details (in templates/archived_pages/)
- Models:
  - `Venda` - Sales transactions
  - `Product` - Product items in sales (shared with products)
- Views:
  - `AddVenda` - Create new sales
  - `SalesList` - List all sales
  - `SaleDetails` - View sale details
- Forms:
  - `VendaForm` - Form for creating sales
  - `ProductFormset` - Inline formset for products in sales

### 4. Championship Management
**Location:** `archived_features/championships/`

**Components:**
- Templates:
  - `campeonatos.html` - Add championship entries
  - `championship_history.html` - Championship history
- Models:
  - `Championship` - Championship entries model
- Views:
  - `AddChampionship` - Add championship entries
  - `ChampionshipDetail` - View championship history
- Forms:
  - `RegisterChampionship` - Form for championship entries

## Backup Files

The following backup files are also included:
- `views_backup.py` - Complete backup of views.py before archiving
- `forms_backup.py` - Complete backup of forms.py before archiving
- `models_backup.py` - Complete backup of models.py before archiving
- `urls_backup.py` - Complete backup of urls.py before archiving

## Restoration Instructions

To restore any of these features:

1. **Restore Models:**
   - Copy the relevant model classes from `models_backup.py` to `models.py`
   - Run `python manage.py makemigrations` and `python manage.py migrate`

2. **Restore Views:**
   - Copy the relevant view classes from `views_backup.py` to `views.py`

3. **Restore Forms:**
   - Copy the relevant form classes from `forms_backup.py` to `forms.py`

4. **Restore URLs:**
   - Copy the relevant URL patterns from `urls_backup.py` to `urls.py`

5. **Restore Templates:**
   - Move the relevant template files from the archived folders back to `focusbjj/templates/`

6. **Restore Static Files:**
   - Move the relevant static files from the archived folders back to `static/`

## Notes

- All archived features have been completely removed from the main application
- The export functionality (`export_xlsx`, `exportar_alunos_xlsx`, `exportar_alunos_total_xlsx`) was preserved as it's still needed for student data export
- The graduation and student management features remain active and functional
- The archived features can be safely restored if needed in the future 