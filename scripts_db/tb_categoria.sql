
CREATE TABLE IF NOT EXISTS tb_categoria
(
    id_peso INT GENERATED ALWAYS AS IDENTITY, 
    cd_categoria INT NOT NULL,
    cd_genero VARCHAR(6) NOT NULL, 
    ds_categoria VARCHAR(50) NOT NULL,
    ds_genero_categoria VARCHAR(50) PRIMARY KEY NOT NULL

);


#Add UNIQUE constraint to column id_peso
ALTER TABLE tb_categoria ADD CONSTRAINT tb_categoria_id_peso_key UNIQUE (id_peso);
