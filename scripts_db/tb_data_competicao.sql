
CREATE TABLE IF NOT EXISTS tb_data_competicao
(
    id_data_competicao INT GENERATED ALWAYS AS IDENTITY, 
    cd_ano INT NOT NULL, 
    cd_mes INT NOT NULL,
    ds_mes VARCHAR(20) NOT NULL, 
    ds_mes_completo VARCHAR(20) NOT NULL,
    PRIMARY KEY (id_data_competicao, cd_mes)

);



