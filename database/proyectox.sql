-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 27-05-2025 a las 02:09:06
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `proyectox`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `capitulos`
--

CREATE TABLE `capitulos` (
  `id` bigint(20) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `contenido` text DEFAULT NULL,
  `curso_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `capitulos`
--

INSERT INTO `capitulos` (`id`, `titulo`, `contenido`, `curso_id`) VALUES
(4, '¿Qué es Gamma IA? ????✨', '<h2>&nbsp;</h2>\r\n<p class=\"ds-markdown-paragraph\"><strong>Gamma IA</strong>&nbsp;es como un&nbsp;<strong>robot inteligente</strong>&nbsp;que usa una tecnolog&iacute;a llamada&nbsp;<strong>Inteligencia Artificial (IA)</strong>&nbsp;para ayudar a las personas a hacer cosas m&aacute;s r&aacute;pido y f&aacute;cil.</p>\r\n<h4><strong>&iquest;Qu&eacute; puede hacer Gamma IA?</strong></h4>\r\n<ol start=\"1\">\r\n<li>\r\n<p class=\"ds-markdown-paragraph\"><strong>Crear presentaciones y documentos</strong>&nbsp;????????:</p>\r\n<ul>\r\n<li>\r\n<p class=\"ds-markdown-paragraph\">Si le dices un tema (como \"los dinosaurios\" o \"el sistema solar\"), Gamma IA puede organizar la informaci&oacute;n y dise&ntilde;ar diapositivas bonitas&nbsp;<strong>&iexcl;en segundos!</strong></p>\r\n</li>\r\n</ul>\r\n</li>\r\n<li>\r\n<p class=\"ds-markdown-paragraph\"><strong>Responder preguntas</strong>&nbsp;❓:</p>\r\n<ul>\r\n<li>\r\n<p class=\"ds-markdown-paragraph\">Es como un&nbsp;<strong>Google m&aacute;s r&aacute;pido</strong>, pero que entiende mejor lo que preguntas y te da respuestas claras.</p>\r\n</li>\r\n</ul>\r\n</li>\r\n<li>\r\n<p class=\"ds-markdown-paragraph\"><strong>Generar ideas</strong>&nbsp;????:</p>\r\n<ul>\r\n<li>\r\n<p class=\"ds-markdown-paragraph\">&iquest;Necesitas un cuento, un ensayo o hasta un juego de palabras? &iexcl;Gamma IA puede inventarlo por ti!</p>\r\n</li>\r\n</ul>\r\n</li>\r\n</ol>\r\n<p><video style=\"display: table; margin-left: auto; margin-right: auto; width: 611px; height: 310px;\" controls=\"controls\" width=\"611\" height=\"310\"> <source src=\"/static/videos/courses/1747425403_CrowdControl_Tutorial.mp4\" type=\"video/mp4\"></video></p>\r\n<h4><strong>&iquest;C&oacute;mo funciona?</strong>&nbsp;????⚡</h4>\r\n<ul>\r\n<li>\r\n<p class=\"ds-markdown-paragraph\"><strong>Aprende de muchos datos</strong>: Imagina que ha le&iacute;do miles de libros y p&aacute;ginas web, por eso sabe de casi todo.</p>\r\n</li>\r\n<li>\r\n<p class=\"ds-markdown-paragraph\"><strong>No piensa como nosotros</strong>: No tiene sentimientos, pero usa matem&aacute;ticas y patrones para simular el lenguaje humano.</p>\r\n</li>\r\n</ul>\r\n<h4><strong>&iquest;Es perfecta?</strong>&nbsp;????</h4>\r\n<p class=\"ds-markdown-paragraph\">&iexcl;No! A veces se equivoca, por eso&nbsp;<strong>siempre debemos revisar</strong>&nbsp;lo que nos dice (como cuando un compa&ntilde;ero te ayuda con la tarea).</p>\r\n<hr>\r\n<h3><strong>Ejemplo para entenderlo mejor</strong>&nbsp;????</h3>\r\n<p class=\"ds-markdown-paragraph\">Imagina que Gamma IA es como un&nbsp;<strong>asistente m&aacute;gico</strong>:</p>\r\n<ul>\r\n<li>\r\n<p class=\"ds-markdown-paragraph\">T&uacute; le dices:&nbsp;<em>\"Hazme 5 diapositivas sobre las ballenas\"</em>&nbsp;????.</p>\r\n</li>\r\n<li>\r\n<p class=\"ds-markdown-paragraph\">&iexcl;Y&nbsp;<em>puf!</em> En un momento crea un resumen con im&aacute;genes y datos interesantes.</p>\r\n</li>\r\n</ul>\r\n<p><img style=\"display: block; margin-left: auto; margin-right: auto;\" src=\"data:image/webp;base64,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\"></p>', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `courses`
--

CREATE TABLE `courses` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `external_url` varchar(255) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `active` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `courses`
--

INSERT INTO `courses` (`id`, `title`, `image_url`, `external_url`, `description`, `created_at`, `updated_at`, `active`) VALUES
(1, 'Gamma IA', 'img/courses/gamma.png', 'https://gamma.app', 'Curso sobre la inteligencia artificial gamma para presentaciones de powerpoint', '2025-04-01 22:54:13', '2025-05-09 11:24:53', 1),
(2, 'Deepseek ', 'img/courses/deepseek.png', 'https://chat.deepseek.com', 'IA chatbot para poder hablar preguntarle cosas varias hacer resúmenes análisis y entre otras cosas investigar la mayoría de las cosas que existen en internet una alternativa totalmente gratuita a chatgpt de uso libre e ilimitado sin embargo menos poderosa ', '2025-05-16 19:32:11', '2025-05-16 19:32:11', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cursos`
--

CREATE TABLE `cursos` (
  `id` bigint(20) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `profesor_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `examenes`
--

CREATE TABLE `examenes` (
  `id` int(11) NOT NULL,
  `capitulo_id` bigint(20) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `tiempo_limite` int(11) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `examenes`
--

INSERT INTO `examenes` (`id`, `capitulo_id`, `titulo`, `descripcion`, `tiempo_limite`, `created_at`, `updated_at`) VALUES
(1, 4, 'Que es gamma', '', 0, '2025-04-10 21:58:07', '2025-04-10 21:58:07');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `metricas_usuarios`
--

CREATE TABLE `metricas_usuarios` (
  `id` bigint(20) NOT NULL,
  `usuario_id` bigint(20) DEFAULT NULL,
  `curso_id` bigint(20) DEFAULT NULL,
  `capitulos_completados` int(11) DEFAULT 0,
  `puntuacion_promedio` decimal(5,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `opciones`
--

CREATE TABLE `opciones` (
  `id` int(11) NOT NULL,
  `pregunta_id` int(11) NOT NULL,
  `texto` text NOT NULL,
  `es_correcta` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `opciones`
--

INSERT INTO `opciones` (`id`, `pregunta_id`, `texto`, `es_correcta`, `created_at`, `updated_at`) VALUES
(1, 1, 'es una ganga', 0, '2025-04-10 21:59:14', '2025-04-10 21:59:14'),
(2, 1, 'es una ia para hacer presentaciones ', 1, '2025-04-10 21:59:31', '2025-04-10 21:59:31'),
(4, 2, 'un programa hecho por seres humano', 0, '2025-05-06 03:52:23', '2025-05-06 03:52:23'),
(5, 2, 'una ia para hacer presentaciones ', 1, '2025-05-06 03:52:46', '2025-05-06 03:52:46');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `preguntas`
--

CREATE TABLE `preguntas` (
  `id` int(11) NOT NULL,
  `examen_id` int(11) NOT NULL,
  `texto` text NOT NULL,
  `tipo` enum('opcion_multiple','verdadero_falso','respuesta_corta') DEFAULT 'opcion_multiple',
  `valor` int(11) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `preguntas`
--

INSERT INTO `preguntas` (`id`, `examen_id`, `texto`, `tipo`, `valor`, `created_at`, `updated_at`) VALUES
(1, 1, 'Que es gamma ?', 'opcion_multiple', 1, '2025-04-10 21:58:44', '2025-04-10 21:58:44'),
(2, 1, 'Es gamma una ia o es algo programado por el mismo ser humano? ', 'opcion_multiple', 5, '2025-05-06 03:51:39', '2025-05-06 03:51:39');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `publicaciones`
--

CREATE TABLE `publicaciones` (
  `id` bigint(20) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `contenido` text DEFAULT NULL,
  `fecha_publicacion` timestamp NOT NULL DEFAULT current_timestamp(),
  `curso_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `respuestas_usuarios`
--

CREATE TABLE `respuestas_usuarios` (
  `id` int(11) NOT NULL,
  `resultado_id` int(11) NOT NULL,
  `pregunta_id` int(11) NOT NULL,
  `opcion_id` int(11) DEFAULT NULL,
  `texto_respuesta` text DEFAULT NULL,
  `es_correcta` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `respuestas_usuarios`
--

INSERT INTO `respuestas_usuarios` (`id`, `resultado_id`, `pregunta_id`, `opcion_id`, `texto_respuesta`, `es_correcta`, `created_at`, `updated_at`) VALUES
(1, 3, 1, 2, NULL, 1, '2025-05-06 04:36:58', '2025-05-06 04:36:58'),
(2, 3, 2, 5, NULL, 1, '2025-05-06 04:36:58', '2025-05-06 04:36:58'),
(3, 4, 1, 2, NULL, 1, '2025-05-09 11:26:28', '2025-05-09 11:26:28'),
(4, 4, 2, 5, NULL, 1, '2025-05-09 11:26:28', '2025-05-09 11:26:28'),
(5, 5, 1, 1, NULL, 0, '2025-05-16 19:00:56', '2025-05-16 19:00:56'),
(6, 5, 2, 5, NULL, 1, '2025-05-16 19:00:56', '2025-05-16 19:00:56');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `resultados_examenes`
--

CREATE TABLE `resultados_examenes` (
  `id` int(11) NOT NULL,
  `usuario_id` bigint(20) NOT NULL,
  `examen_id` int(11) NOT NULL,
  `puntuacion` decimal(5,2) DEFAULT 0.00,
  `fecha_inicio` timestamp NOT NULL DEFAULT current_timestamp(),
  `fecha_fin` timestamp NULL DEFAULT NULL,
  `completado` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `resultados_examenes`
--

INSERT INTO `resultados_examenes` (`id`, `usuario_id`, `examen_id`, `puntuacion`, `fecha_inicio`, `fecha_fin`, `completado`, `created_at`, `updated_at`) VALUES
(3, 1, 1, 100.00, '2025-05-06 04:36:39', '2025-05-06 04:36:59', 1, '2025-05-06 04:36:39', '2025-05-06 04:36:59'),
(4, 1, 1, 100.00, '2025-05-06 04:38:44', '2025-05-09 11:26:28', 1, '2025-05-06 04:38:44', '2025-05-09 11:26:28'),
(5, 1, 1, 83.33, '2025-05-16 19:00:49', '2025-05-16 19:00:56', 1, '2025-05-16 19:00:49', '2025-05-16 19:00:56');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tiempo_observacion`
--

CREATE TABLE `tiempo_observacion` (
  `id` bigint(20) NOT NULL,
  `usuario_id` bigint(20) DEFAULT NULL,
  `curso_id` bigint(20) DEFAULT NULL,
  `tiempo_total` time NOT NULL DEFAULT '00:00:00',
  `ultima_actividad` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` bigint(20) NOT NULL,
  `nombre_usuario` varchar(255) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `tipo_usuario` enum('estudiante','profesor') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre_usuario`, `contraseña`, `tipo_usuario`) VALUES
(1, 'sanctusrtx', 'scrypt:32768:8:1$MExR26FaqLhAGOOb$a5fa534c1d866969860f23a0b214502bd8e9796c0b8096fd7094f63636be17fac476ae44dc1e925f0425072ad220082e875cb3ba521ac2abb148df4cc5dd68ee', 'profesor'),
(2, 'admin_profesor', 'Admin2025!', 'profesor');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `capitulos`
--
ALTER TABLE `capitulos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `curso_id` (`curso_id`);

--
-- Indices de la tabla `courses`
--
ALTER TABLE `courses`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `cursos`
--
ALTER TABLE `cursos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `profesor_id` (`profesor_id`);

--
-- Indices de la tabla `examenes`
--
ALTER TABLE `examenes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `capitulo_id` (`capitulo_id`);

--
-- Indices de la tabla `metricas_usuarios`
--
ALTER TABLE `metricas_usuarios`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `curso_id` (`curso_id`);

--
-- Indices de la tabla `opciones`
--
ALTER TABLE `opciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `pregunta_id` (`pregunta_id`);

--
-- Indices de la tabla `preguntas`
--
ALTER TABLE `preguntas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `examen_id` (`examen_id`);

--
-- Indices de la tabla `publicaciones`
--
ALTER TABLE `publicaciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `curso_id` (`curso_id`);

--
-- Indices de la tabla `respuestas_usuarios`
--
ALTER TABLE `respuestas_usuarios`
  ADD PRIMARY KEY (`id`),
  ADD KEY `resultado_id` (`resultado_id`),
  ADD KEY `pregunta_id` (`pregunta_id`),
  ADD KEY `opcion_id` (`opcion_id`);

--
-- Indices de la tabla `resultados_examenes`
--
ALTER TABLE `resultados_examenes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `examen_id` (`examen_id`);

--
-- Indices de la tabla `tiempo_observacion`
--
ALTER TABLE `tiempo_observacion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `curso_id` (`curso_id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre_usuario` (`nombre_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `capitulos`
--
ALTER TABLE `capitulos`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `courses`
--
ALTER TABLE `courses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `cursos`
--
ALTER TABLE `cursos`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `examenes`
--
ALTER TABLE `examenes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `metricas_usuarios`
--
ALTER TABLE `metricas_usuarios`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `opciones`
--
ALTER TABLE `opciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `preguntas`
--
ALTER TABLE `preguntas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `publicaciones`
--
ALTER TABLE `publicaciones`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `respuestas_usuarios`
--
ALTER TABLE `respuestas_usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `resultados_examenes`
--
ALTER TABLE `resultados_examenes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `tiempo_observacion`
--
ALTER TABLE `tiempo_observacion`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `cursos`
--
ALTER TABLE `cursos`
  ADD CONSTRAINT `cursos_ibfk_1` FOREIGN KEY (`profesor_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `examenes`
--
ALTER TABLE `examenes`
  ADD CONSTRAINT `examenes_ibfk_1` FOREIGN KEY (`capitulo_id`) REFERENCES `capitulos` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `metricas_usuarios`
--
ALTER TABLE `metricas_usuarios`
  ADD CONSTRAINT `metricas_usuarios_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `metricas_usuarios_ibfk_2` FOREIGN KEY (`curso_id`) REFERENCES `cursos` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `opciones`
--
ALTER TABLE `opciones`
  ADD CONSTRAINT `opciones_ibfk_1` FOREIGN KEY (`pregunta_id`) REFERENCES `preguntas` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `preguntas`
--
ALTER TABLE `preguntas`
  ADD CONSTRAINT `preguntas_ibfk_1` FOREIGN KEY (`examen_id`) REFERENCES `examenes` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `publicaciones`
--
ALTER TABLE `publicaciones`
  ADD CONSTRAINT `publicaciones_ibfk_1` FOREIGN KEY (`curso_id`) REFERENCES `cursos` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `respuestas_usuarios`
--
ALTER TABLE `respuestas_usuarios`
  ADD CONSTRAINT `respuestas_usuarios_ibfk_1` FOREIGN KEY (`resultado_id`) REFERENCES `resultados_examenes` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `respuestas_usuarios_ibfk_2` FOREIGN KEY (`pregunta_id`) REFERENCES `preguntas` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `respuestas_usuarios_ibfk_3` FOREIGN KEY (`opcion_id`) REFERENCES `opciones` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `resultados_examenes`
--
ALTER TABLE `resultados_examenes`
  ADD CONSTRAINT `resultados_examenes_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `resultados_examenes_ibfk_2` FOREIGN KEY (`examen_id`) REFERENCES `examenes` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `tiempo_observacion`
--
ALTER TABLE `tiempo_observacion`
  ADD CONSTRAINT `tiempo_observacion_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `tiempo_observacion_ibfk_2` FOREIGN KEY (`curso_id`) REFERENCES `cursos` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
