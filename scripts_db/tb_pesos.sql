
CREATE TABLE IF NOT EXISTS tb_pesos
(
    id_peso INT GENERATED ALWAYS AS IDENTITY, 
    cd_genero VARCHAR(6) NOT NULL, 
    ds_categoria VARCHAR(50) NOT NULL,
    ds_genero_categoria VARCHAR(50) PRIMARY KEY NOT NULL

);



