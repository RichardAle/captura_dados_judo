
CREATE TABLE IF NOT EXISTS tb_judoca_lista
(
    id_judoca INT NOT NULL, 
    nm_judoca varchar(100) NOT NULL,
    ds_link_foto VARCHAR(200) NOT NULL, 
    ds_link_perfil VARCHAR(200) NOT NULL, 
    ds_link_resultado VARCHAR(200) NOT NULL, 
    ds_link_disputa VARCHAR(200) NOT NULL, 
    ds_link_estatistica VARCHAR(200) NOT NULL,
    id_peso INT CONSTRAINT fk_peso_judoca REFERENCES tb_categoria(id_peso),
    id_pais INT CONSTRAINT fk_pais_judoca REFERENCES tb_pais(id_pais),
    PRIMARY KEY (id_judoca, id_peso)
);



