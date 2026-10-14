-- O local do sensor vem da coluna out/in e a base não tem device_id.
CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
SELECT tipo_sensor, ROUND(AVG(temperatura)::numeric, 2) AS avg_temp,
       COUNT(*) AS total_leituras
FROM temperature_readings
GROUP BY tipo_sensor;

CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT EXTRACT(HOUR FROM data_leitura)::int AS hora,
       COUNT(*) AS contagem
FROM temperature_readings
GROUP BY EXTRACT(HOUR FROM data_leitura)
ORDER BY hora;

CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT data_leitura::date AS data,
       MIN(temperatura) AS temp_min,
       MAX(temperatura) AS temp_max
FROM temperature_readings
GROUP BY data_leitura::date
ORDER BY data;
