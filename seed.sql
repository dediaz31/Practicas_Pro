-- seed.sql — Seed data para PrácticasPro
-- Ejecutar en Supabase SQL Editor si la conexión directa por Postgres falla.

BEGIN;

CREATE TABLE IF NOT EXISTS empresas (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(150) NOT NULL,
  nit VARCHAR(20) NOT NULL UNIQUE,
  sector VARCHAR(50) NOT NULL,
  ciudad VARCHAR(80) NOT NULL,
  direccion VARCHAR(200),
  sitio_web VARCHAR(200),
  descripcion TEXT,
  logo VARCHAR(500),
  contacto_nombre VARCHAR(100),
  contacto_email VARCHAR(150),
  activo BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS estudiantes (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  correo VARCHAR(150) NOT NULL UNIQUE,
  semestre INTEGER NOT NULL,
  programa VARCHAR(100) DEFAULT 'Ingeniería de Sistemas',
  telefono VARCHAR(20),
  ciudad VARCHAR(80) DEFAULT 'Bogotá',
  foto_perfil VARCHAR(500),
  hoja_vida VARCHAR(500),
  activo BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS vacantes (
  id SERIAL PRIMARY KEY,
  titulo VARCHAR(150) NOT NULL,
  descripcion TEXT NOT NULL,
  requisitos TEXT,
  salario NUMERIC(12,2),
  modalidad VARCHAR(50) NOT NULL,
  duracion_meses INTEGER DEFAULT 6,
  cupos INTEGER DEFAULT 1,
  activa BOOLEAN DEFAULT TRUE,
  empresa_id INTEGER NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS postulaciones (
  id SERIAL PRIMARY KEY,
  estudiante_id INTEGER NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
  vacante_id INTEGER NOT NULL REFERENCES vacantes(id) ON DELETE CASCADE,
  estado VARCHAR(50) DEFAULT 'Pendiente',
  carta_motivacion TEXT,
  notas_evaluador TEXT,
  fecha_postulacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO empresas (id, nombre, nit, sector, ciudad, sitio_web, descripcion, contacto_nombre, contacto_email, created_at, updated_at)
VALUES
  (1, 'Bancolombia S.A.', '890903938-8', 'Finanzas', 'Medellín', 'https://www.grupobancolombia.com', 'Banco líder en Colombia con presencia en toda Latinoamérica.', 'Ana María Restrepo', 'practicas@bancolombia.com.co', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (2, 'Grupo Bolívar - Davivienda', '860034313-7', 'Finanzas', 'Bogotá', 'https://www.davivienda.com', 'Entidad financiera del Grupo Bolívar con amplia cobertura nacional.', 'Carlos Pineda', 'talento@davivienda.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (3, 'Mercado Libre Colombia', '900123456-1', 'Tecnología', 'Bogotá', 'https://www.mercadolibre.com.co', 'Plataforma líder de e-commerce y servicios financieros digitales en LATAM.', 'Laura Gómez', 'early.talent@mercadolibre.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (4, 'Rappi Inc.', '901234567-2', 'Tecnología', 'Bogotá', 'https://www.rappi.com', 'Superapp colombiana de delivery y servicios on-demand.', 'Sebastián Torres', 'internships@rappi.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (5, 'Clínica Shaio', '860003166-5', 'Salud', 'Bogotá', 'https://www.shaio.org', 'Centro médico especializado de referencia nacional en cardiología.', 'Patricia Vargas', 'rrhh@shaio.org', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (6, 'Ecopetrol S.A.', '899999068-1', 'Manufactura', 'Bogotá', 'https://www.ecopetrol.com.co', 'Empresa petrolera más grande de Colombia.', 'Fernando Ríos', 'talentohumano@ecopetrol.com.co', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (7, 'Deloitte Colombia', '860001022-3', 'Consultoría', 'Bogotá', 'https://www2.deloitte.com/co', 'Firma global de auditoría, consultoría y servicios profesionales.', 'Valeria Castro', 'campus@deloitte.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (id) DO NOTHING;

INSERT INTO vacantes (id, titulo, descripcion, requisitos, salario, modalidad, duracion_meses, cupos, activa, empresa_id, created_at, updated_at)
VALUES
  (1, 'Practicante de Desarrollo Backend', 'Desarrollarás microservicios en Python/FastAPI para la plataforma de pagos.', 'Python, FastAPI, Git, PostgreSQL, Docker básico, inglés intermedio', 1800000.00, 'Híbrido', 6, 3, TRUE, 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (2, 'Practicante QA / Automatización', 'Diseñarás y ejecutarás casos de prueba. Aprenderás automatización con Selenium y Cypress.', 'Fundamentos de QA, Selenium o Cypress, SQL básico, metodologías ágiles', 1600000.00, 'Remoto', 6, 2, TRUE, 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (3, 'Practicante Analítica de Datos', 'Apoyarás el equipo de BI analizando datos de transacciones y construyendo dashboards en Power BI.', 'Python, Power BI, SQL avanzado, estadística básica', 1700000.00, 'Presencial', 6, 2, TRUE, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (4, 'Practicante de Ciberseguridad', 'Participarás en el SOC monitoreando amenazas y apoyando auditorías de compliance ISO 27001.', 'Redes TCP/IP, Linux, fundamentos de seguridad, SIEM básico', 1900000.00, 'Presencial', 6, 1, TRUE, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (5, 'Practicante de Desarrollo Móvil Android', 'Contribuirás al desarrollo de la app de Rappi con más de 10 millones de usuarios.', 'Kotlin, Android Studio, Jetpack Compose, Git, inglés básico', 2000000.00, 'Híbrido', 6, 2, TRUE, 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (6, 'Practicante de UX/UI Design', 'Diseñarás interfaces para productos digitales, realizando investigación con usuarios y prototipos en Figma.', 'Figma, Adobe XD, investigación UX, prototipado, portafolio de diseño', 1500000.00, 'Híbrido', 6, 2, TRUE, 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (7, 'Practicante de Infraestructura Cloud', 'Apoyarás la migración de sistemas a AWS/Azure con Terraform y Docker.', 'Linux, Docker, AWS o Azure básico, redes, Python o Bash', 2100000.00, 'Presencial', 6, 1, TRUE, 6, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (8, 'Practicante de Consultoría Tecnológica', 'Participarás en proyectos de transformación digital para clientes de sectores financiero y retail.', 'Excel avanzado, PowerPoint, análisis de negocio, inglés intermedio-alto', 1800000.00, 'Presencial', 6, 3, TRUE, 7, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (9, 'Practicante de Sistemas de Información', 'Apoyarás la gestión de sistemas core bancarios participando en proyectos TI bajo metodología PMI.', 'SQL Server, análisis de requerimientos, BPMN, gestión de proyectos', 1650000.00, 'Presencial', 6, 2, TRUE, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (10, 'Practicante de Data Science', 'Desarrollarás modelos de machine learning para proyectos de analítica avanzada.', 'Python, scikit-learn, pandas, SQL, estadística, inglés intermedio', 2000000.00, 'Híbrido', 6, 2, TRUE, 7, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (id) DO NOTHING;

INSERT INTO estudiantes (id, nombre, correo, semestre, programa, ciudad, telefono, activo, created_at, updated_at)
VALUES
  (1, 'Deiby Alejandro Hernández', 'da.hernandez@ucatolica.edu.co', 9, 'Ingeniería de Sistemas y Computación', 'Bogotá', '+57 310 234 5678', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (2, 'María Camila Torres Ruiz', 'mc.torres@ucatolica.edu.co', 9, 'Ingeniería de Sistemas y Computación', 'Bogotá', '+57 311 345 6789', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (3, 'Juan Sebastián López Vargas', 'js.lopez@ucatolica.edu.co', 8, 'Ingeniería de Sistemas y Computación', 'Bogotá', '+57 312 456 7890', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (4, 'Valentina Pérez Morales', 'v.perez@ucatolica.edu.co', 10, 'Ingeniería de Sistemas y Computación', 'Bogotá', '+57 313 567 8901', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (5, 'Andrés Felipe Gómez Suárez', 'af.gomez@ucatolica.edu.co', 9, 'Ingeniería de Sistemas y Computación', 'Soacha', '+57 314 678 9012', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (6, 'Laura Daniela Sánchez Castro', 'ld.sanchez@ucatolica.edu.co', 8, 'Ingeniería de Sistemas y Computación', 'Bogotá', '+57 315 789 0123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (7, 'Oscar Iván Rivera Mayorga', 'oi.rivera@ucatolica.edu.co', 9, 'Ingeniería de Sistemas y Computación', 'Bogotá', '+57 316 890 1234', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (8, 'Natalia Alejandra Díaz Forero', 'na.diaz@ucatolica.edu.co', 10, 'Ingeniería de Sistemas y Computación', 'Bogotá', '+57 317 901 2345', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (9, 'Santiago Hernán Martínez Peña', 'sh.martinez@ucatolica.edu.co', 7, 'Ingeniería de Sistemas y Computación', 'Chía', '+57 318 012 3456', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (10, 'Luisa Fernanda Rojas Méndez', 'lf.rojas@ucatolica.edu.co', 9, 'Ingeniería de Sistemas y Computación', 'Bogotá', '+57 319 123 4567', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (id) DO NOTHING;

INSERT INTO postulaciones (id, estudiante_id, vacante_id, estado, carta_motivacion, notas_evaluador, fecha_postulacion, updated_at)
VALUES
  (1, 1, 1, 'Entrevista', 'Tengo experiencia en QA Testing y desarrollo con FastAPI. Me interesa aplicar mis conocimientos en Mercado Libre.', 'Candidato con buen perfil técnico. Programar entrevista técnica.', NOW() - INTERVAL '5 days', NOW() - INTERVAL '5 days'),
  (2, 1, 2, 'Aceptado', 'He trabajado en QA para una fintech durante 1 año. Manejo Cypress y tengo certificación SFPC.', 'Perfil excelente. Experiencia real en QA fintech. ACEPTADO.', NOW() - INTERVAL '10 days', NOW() - INTERVAL '10 days'),
  (3, 2, 3, 'En Revisión', 'Me apasiona el análisis de datos. Tengo proyectos de Power BI y Python en mi portafolio.', NULL, NOW() - INTERVAL '7 days', NOW() - INTERVAL '7 days'),
  (4, 2, 10, 'Pendiente', 'Estoy desarrollando mi tesis en machine learning aplicado a finanzas.', NULL, NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days'),
  (5, 3, 7, 'Pendiente', 'Tengo conocimientos de AWS y Docker. Me gustaría aprender IaC en un proyecto real.', NULL, NOW() - INTERVAL '12 days', NOW() - INTERVAL '12 days'),
  (6, 3, 1, 'Rechazado', 'Me interesa el backend con Python.', 'No cumple requisito de inglés intermedio.', NOW() - INTERVAL '15 days', NOW() - INTERVAL '15 days'),
  (7, 4, 6, 'Entrevista', 'Tengo portafolio de diseño en Figma. He trabajado en proyectos universitarios de UX Research.', 'Portafolio sólido. Avanzar a entrevista con el equipo de diseño.', NOW() - INTERVAL '8 days', NOW() - INTERVAL '8 days'),
  (8, 4, 8, 'Pendiente', 'Me interesa la consultoría tecnológica para combinar habilidades técnicas y de negocio.', NULL, NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days'),
  (9, 5, 5, 'En Revisión', 'Desarrollo apps Android con Kotlin y Jetpack Compose. Tengo una app publicada en Play Store.', 'Revisar portafolio. Tiene app publicada, diferenciador importante.', NOW() - INTERVAL '20 days', NOW() - INTERVAL '20 days'),
  (10, 6, 9, 'Aceptado', 'Tengo buen manejo de SQL Server y gestión de proyectos TI.', 'Aprobada. Inicia 15 de julio.', NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day'),
  (11, 7, 1, 'Pendiente', 'Experiencia en FastAPI y PostgreSQL en proyectos universitarios.', NULL, NOW() - INTERVAL '18 days', NOW() - INTERVAL '18 days'),
  (12, 8, 10, 'Entrevista', 'Tesis en modelos predictivos para retail. Domino Python y scikit-learn.', 'Perfil muy fuerte en ML. Entrevista agendada.', NOW() - INTERVAL '9 days', NOW() - INTERVAL '9 days'),
  (13, 9, 2, 'Pendiente', 'Aprendiendo FastAPI y Docker. Me gustaría ganar experiencia real.', NULL, NOW() - INTERVAL '4 days', NOW() - INTERVAL '4 days'),
  (14, 10, 3, 'En Revisión', 'Me interesa la analítica de datos y tengo bases sólidas en Python.', NULL, NOW() - INTERVAL '6 days', NOW() - INTERVAL '6 days')
ON CONFLICT (id) DO NOTHING;

COMMIT;
