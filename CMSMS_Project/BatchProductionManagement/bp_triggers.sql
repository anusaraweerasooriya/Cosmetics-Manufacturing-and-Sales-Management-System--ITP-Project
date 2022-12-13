use cmsms_db;
DELIMITER //
DROP TRIGGER IF EXISTS after_rawmaterial_insert//
create trigger after_rawmaterial_insert
    before insert
    on batchproductionmanagement_rawmaterial
    for each row
begin
    insert into batchproductionmanagement_rawmaterialhistory(name, quantity, reorder_level, last_updated, action)
    VALUES (NEW.name, NEW.quantity, NEW.reorder_level, CURDATE(), 'Added');
end//

DROP TRIGGER IF EXISTS after_rawmaterial_update//
create trigger after_rawmaterial_update
    before update
    on batchproductionmanagement_rawmaterial
    for each row
begin
    insert into batchproductionmanagement_rawmaterialhistory(name, quantity, reorder_level, last_updated, action)
    VALUES (NEW.name, NEW.quantity, NEW.reorder_level, CURDATE(), 'Updated');
end//

DROP TRIGGER IF EXISTS after_rawmaterial_delete//
create trigger after_rawmaterial_delete
    before delete
    on batchproductionmanagement_rawmaterial
    for each row
begin
    insert into batchproductionmanagement_rawmaterialhistory(name, quantity, reorder_level, last_updated, action)
    VALUES (OLD.name, OLD.quantity, OLD.reorder_level, CURDATE(), 'Deleted');
end//

DELIMITER ;