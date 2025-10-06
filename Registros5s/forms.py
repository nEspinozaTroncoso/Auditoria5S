RESPONSABLES = [
    "USUARIO_1",
    "USUARIO_2",
    "USUARIO_3",
]
AREAS = [
    "AREA_1",
    "AREA_2",
    "AREA_3",
]

secciones = {
    "Seiri / Clasificar": [
        {
            "pregunta": "¿Hay residuos/envases en la zona? (items)",
            "opciones": [
                {"texto": "0", "valor": 100},
                {"texto": "1", "valor": 75},
                {"texto": "2", "valor": 50},
                {"texto": "3", "valor": 25},
                {"texto": "4+", "valor": 0},
            ],
        },
        {
            "pregunta": "¿Hay materias primas (no WIP) en los pasillos? (items)",
            "opciones": [
                {"texto": "0", "valor": 100},
                {"texto": "1", "valor": 75},
                {"texto": "2", "valor": 50},
                {"texto": "3", "valor": 25},
                {"texto": "4+", "valor": 0},
            ],
        },
        {
            "pregunta": "¿Hay transporte/equipos mal ubicados en la zona? (items)",
            "opciones": [
                {"texto": "0", "valor": 100},
                {"texto": "1", "valor": 50},
                {"texto": "2+", "valor": 0},
            ],
        },
    ],
    "Seiton / Ordenar": [
        {
            "pregunta": "¿Hay estaciones de basura/limpieza en el área?",
            "opciones": [
                {
                    "texto": "Estaciones de residuos y limpieza instaladas, definidas y utilizadas",
                    "valor": 100,
                },
                {
                    "texto": "Estaciones de residuos y limpieza en su lugar, definidas pero parcialmente utilizadas.",
                    "valor": 75,
                },
                {
                    "texto": "Estaciones en su luga e indicadas pero no utilizadas",
                    "valor": 50,
                },
                {
                    "texto": "Residuos recogidos en un contenedor sin marcar.",
                    "valor": 25,
                },
                {"texto": "Ninguna", "valor": 0},
            ],
        },
        {
            "pregunta": "¿Hay estaciones de seguridad en el área o cercana a esta?",
            "opciones": [
                {
                    "texto": "Estaciones de seguridad instaladas, definidas, abastecidas y utilizadas",
                    "valor": 100,
                },
                {
                    "texto": "Estaciones en su lugar e indicadas pero parcialmente abastecidas/utilizadas",
                    "valor": 50,
                },
                {"texto": "Ninguna", "valor": 0},
            ],
        },
        {
            "pregunta": "¿Existe un área definida de suministro y/o espera de RM/WIP?",
            "opciones": [
                {
                    "texto": "Área indicada para RM y WIP utilizados correctamente",
                    "valor": 100,
                },
                {
                    "texto": "Ubicaciones definidas pero no utilizadas correctamente",
                    "valor": 50,
                },
                {"texto": "Ninguna", "valor": 0},
            ],
        },
    ],
    "Seiso / Limpiar": [
        {
            "pregunta": "¿El área está limpia?",
            "opciones": [
                {"texto": "0", "valor": 0},
                {"texto": "1", "valor": 25},
                {"texto": "2", "valor": 50},
                {"texto": "3", "valor": 75},
                {"texto": "4", "valor": 100},
            ],
        },
        {
            "pregunta": "¿Se detectan problemas de limpieza?",
            "opciones": [
                {"texto": "Cumple", "valor": 100},
                {"texto": "No cumple", "valor": 0},
            ],
        },
    ],
    "Seiketsu / estandarizar": [
        {
            "pregunta": "¿Se mantienen estándares visuales?",
            "opciones": [
                {"texto": "0", "valor": 0},
                {"texto": "1", "valor": 25},
                {"texto": "2", "valor": 50},
                {"texto": "3", "valor": 75},
                {"texto": "4", "valor": 100},
            ],
        },
        {
            "pregunta": "¿Existen reglas claras para mantener el orden?",
            "opciones": [
                {"texto": "Sí", "valor": 100},
                {"texto": "No", "valor": 0},
            ],
        },
    ],
    "Shitsuke / Mantener": [
        {
            "pregunta": "¿Se cumple con la disciplina de las 5S?",
            "opciones": [
                {"texto": "0", "valor": 0},
                {"texto": "1", "valor": 25},
                {"texto": "2", "valor": 50},
                {"texto": "3", "valor": 75},
                {"texto": "4", "valor": 100},
            ],
        },
        {
            "pregunta": "¿El personal sigue los procedimientos?",
            "opciones": [
                {"texto": "Cumple", "valor": 100},
                {"texto": "No cumple", "valor": 0},
            ],
        },
    ],
    "Seguridad": [
        {
            "pregunta": "¿Se usan los EPP correctamente?",
            "opciones": [
                {"texto": "0", "valor": 0},
                {"texto": "1", "valor": 25},
                {"texto": "2", "valor": 50},
                {"texto": "3", "valor": 75},
                {"texto": "4", "valor": 100},
            ],
        },
        {
            "pregunta": "¿Existen riesgos visibles?",
            "opciones": [
                {"texto": "Sí", "valor": 0},
                {"texto": "No", "valor": 100},
            ],
        },
    ],
}
