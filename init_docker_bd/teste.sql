
CREATE TABLE `banco_alunos` (
  `nome` varchar(50) DEFAULT NULL,
  `RM` char(5) NOT NULL,
  `codetec` char(3) DEFAULT NULL,
  `sala` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`RM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `cadastro_aluno` (
  `RM` char(5) NOT NULL,
  `senha` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`RM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `salas` (
  `nome_sala` varchar(50) NOT NULL,
  `codetec` char(3) NOT NULL,
  `id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
