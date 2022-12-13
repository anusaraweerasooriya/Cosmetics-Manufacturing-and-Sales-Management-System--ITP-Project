use cmsms_db;
DELIMITER //
DROP TRIGGER IF EXISTS after_product_insert//
create trigger after_product_insert
    before insert
    on formulationandlabmanagement_products
    for each row
begin
    insert into formulationandlabmanagement_products_history(product_name, product_category, description, preparation_method, duration, product_image, date , action) 
    VALUES (NEW.product_name, NEW.product_category, NEW.description, NEW.preparation_method, NEW.duration, NEW.product_image, CURDATE(), 'Added');
end//

DROP TRIGGER IF EXISTS after_product_update//
create trigger after_product_update
    before update
    on formulationandlabmanagement_products
    for each row
begin
    insert into formulationandlabmanagement_products_history(product_name, product_category, description, preparation_method, duration, product_image, date , action)  
    VALUES (NEW.product_name, NEW.product_category, NEW.description, NEW.preparation_method, NEW.duration, NEW.product_image, CURDATE(), 'Updated');
end//

DROP TRIGGER IF EXISTS after_product_delete//
create trigger after_product_delete
    before delete
    on formulationandlabmanagement_products
    for each row
begin
    insert into formulationandlabmanagement_products_history(product_name, product_category, description, preparation_method, duration, product_image, date , action)
    VALUES (OLD.product_name, OLD.product_category, OLD.description, OLD.preparation_method, OLD.duration, OLD.product_image, CURDATE(), 'Deleted');
end//

DELIMITER ;