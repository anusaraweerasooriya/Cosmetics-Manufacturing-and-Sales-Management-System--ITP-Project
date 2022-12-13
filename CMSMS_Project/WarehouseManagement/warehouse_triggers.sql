create trigger raw_history_insert
    before insert
    on warehousemanagement_rawmaterial
    for each row
begin
    insert into warehousemanagement_history(itemID, itemName, quantity, create_date, action, affect_table) VALUES (NEW.itemID, NEW.itemName, NEW.quantity, CURDATE(), 'Inserted', 'Raw Materials');
end;

create trigger raw_history_update
    before update
    on warehousemanagement_rawmaterial
    for each row
begin
    insert into warehousemanagement_history(itemID, itemName, quantity, create_date, action, affect_table ) VALUES (NEW.itemID, NEW.itemName, NEW.quantity, CURDATE(), 'Updated', 'Raw Materials');
end;

create trigger raw_history_delete
    before delete
    on warehousemanagement_rawmaterial
    for each row
begin
    insert into warehousemanagement_history(itemID, itemName, quantity, create_date, action, affect_table) VALUES (OLD.itemID, old.itemName, OLD.quantity, CURDATE(), 'Deleted', 'Raw Materials');
end;

create trigger equipment_history_insert
    before insert
    on warehousemanagement_equipment
    for each row
begin
    insert into warehousemanagement_history(itemID, itemName, quantity, create_date, action, affect_table) VALUES (NEW.itemID, NEW.itemName, NEW.quantity, CURDATE(), 'Inserted', 'Equipments');
end;

create trigger equipment_history_update
    before update
    on warehousemanagement_equipment
    for each row
begin
    insert into warehousemanagement_history(itemID, itemName, quantity, create_date, action, affect_table ) VALUES (NEW.itemID, NEW.itemName, NEW.quantity, CURDATE(), 'Updated', 'Equipments');
end;

create trigger equipment_history_delete
    before delete
    on warehousemanagement_equipment
    for each row
begin
    insert into warehousemanagement_history(itemID, itemName, quantity, create_date, action, affect_table) VALUES (OLD.itemID, old.itemName, OLD.quantity, CURDATE(), 'Deleted', 'Equipments');
end;

create trigger packaging_history_insert
    before insert
    on warehousemanagement_packaging
    for each row
begin
    insert into warehousemanagement_history(itemID, itemName, quantity, create_date, action, affect_table) VALUES (NEW.itemID, NEW.itemName, NEW.quantity, CURDATE(), 'Inserted', 'Packaging');
end;

create trigger packaging_history_update
    before update
    on warehousemanagement_packaging
    for each row
begin
    insert into warehousemanagement_history(itemID, itemName, quantity, create_date, action, affect_table ) VALUES (NEW.itemID, NEW.itemName, NEW.quantity, CURDATE(), 'Updated', 'Packaging');
end;

create trigger packaging_history_delete
    before delete
    on warehousemanagement_packaging
    for each row
begin
    insert into warehousemanagement_history(itemID, itemName, quantity, create_date, action, affect_table) VALUES (OLD.itemID, old.itemName, OLD.quantity, CURDATE(), 'Deleted', 'Packaging');
end;

drop trigger raw_history_delete;
drop trigger raw_history_insert;
drop trigger raw_history_update;
drop trigger equipment_history_delete;
drop trigger equipment_history_insert;
drop trigger equipment_history_update;