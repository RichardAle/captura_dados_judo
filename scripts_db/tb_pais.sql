
CREATE TABLE IF NOT EXISTS tb_pais
(
    id_pais INT GENERATED ALWAYS AS IDENTITY, \
    cd_atributo_pais INT NOT NULL,
    cd_pais VARCHAR(3) PRIMARY KEY NOT NULL, 
    nm_pais VARCHAR(50) NOT NULL, 
    ds_pais VARCHAR(53) NOT NULL
);

#Add UNIQUE constraint to column id_pais
ALTER TABLE tb_pais ADD CONSTRAINT tb_pais_id_pais_key UNIQUE (id_pais);


