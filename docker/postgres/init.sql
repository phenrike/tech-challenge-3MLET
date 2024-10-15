
CREATE TABLE producao (
    id_producao SERIAL PRIMARY KEY,
    ds_produto VARCHAR(255) NOT NULL,
    tp_produto VARCHAR(50) NOT NULL,
    dt_ano INTEGER NOT NULL,
    qt_producao FLOAT NOT NULL
);

INSERT INTO producao (ds_Produto, tp_Produto, dt_Ano, qt_Producao)
VALUES ('Arroz', 'Cereal', 2023, 1500.75);