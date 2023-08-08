
CREATE TABLE IF NOT EXISTS tb_perfil
(
    id_judoca INT PRIMARY KEY,
    nm_familia VARCHAR(50),
    nm_judoca VARCHAR(50), 
    ds_genero VARCHAR(50) NOT NULL, 
    vl_idade int, 
    ds_categoria VARCHAR(50) NOT NULL,
    ds_tecnica_favorita VARCHAR(50)
);


