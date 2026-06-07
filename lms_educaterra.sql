-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost:8889
-- Généré le : dim. 07 juin 2026 à 22:12
-- Version du serveur : 8.0.44
-- Version de PHP : 8.3.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `lms_educaterra`
--

-- --------------------------------------------------------

--
-- Structure de la table `activites`
--

CREATE TABLE `activites` (
  `id` int NOT NULL,
  `id_apprenant` int NOT NULL,
  `sport` varchar(100) NOT NULL,
  `date_pratique` date NOT NULL,
  `evaluation` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `cours`
--

CREATE TABLE `cours` (
  `id` int NOT NULL,
  `titre` varchar(100) NOT NULL,
  `contenu` text NOT NULL,
  `id_formateur` int NOT NULL,
  `date_creation` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `fiches_journalieres`
--

CREATE TABLE `fiches_journalieres` (
  `id` int NOT NULL,
  `id_formateur` int NOT NULL,
  `date` date NOT NULL,
  `contenu` text NOT NULL,
  `id_groupe` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `parcours`
--

CREATE TABLE `parcours` (
  `id` int NOT NULL,
  `intitule` varchar(50) NOT NULL,
  `description` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `parcours`
--

INSERT INTO `parcours` (`id`, `intitule`, `description`) VALUES
(1, 'BPJEPS', 'Brevet Professionnel de la Jeunesse, de l\'Éducation Populaire et du Sport'),
(2, 'MAPST', 'Mention complémentaire Animation et Sport'),
(3, 'AAN', 'Animateur Activités Nautiques'),
(4, 'ASEC', 'Animateur Sportif Enfants et Collectivités');

-- --------------------------------------------------------

--
-- Structure de la table `quizz`
--

CREATE TABLE `quizz` (
  `id` int NOT NULL,
  `id_cours` int NOT NULL,
  `question` text NOT NULL,
  `reponse_correcte` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `resultats_quizz`
--

CREATE TABLE `resultats_quizz` (
  `id` int NOT NULL,
  `id_apprenant` int NOT NULL,
  `id_quizz` int NOT NULL,
  `score` float NOT NULL,
  `date_passage` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `utilisateurs`
--

CREATE TABLE `utilisateurs` (
  `id` int NOT NULL,
  `nom` varchar(50) NOT NULL,
  `prenom` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `mot_de_passe` varchar(255) NOT NULL,
  `role` enum('administrateur','formateur','apprenant') NOT NULL,
  `id_parcours` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `utilisateurs`
--

INSERT INTO `utilisateurs` (`id`, `nom`, `prenom`, `email`, `mot_de_passe`, `role`, `id_parcours`) VALUES
(1, 'Admin', 'System', 'admin@educaterra.fr', '$2b$12$ZdB6uDq8Mg5tU5HHJHHGA.OAZfU/CYB8EOOuJJSJWr5Qfqwl.ZWTW', 'administrateur', NULL),
(2, 'Dupont', 'Jean', 'formateur@educaterra.fr', '$2b$12$Yr9iLDu7tgmn0EAfLhX3Ku3uFmzVI1GOwVAlcYTzT0YJRrJqT2WWu', 'formateur', NULL),
(3, 'Martin', 'Léa', 'apprenant@educaterra.fr', '$2b$12$4v9u6zLJzI4thH1x8z0sFOtTB2bZITOzsn7FqaEAeavShSkt44Z1i', 'apprenant', 1);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `activites`
--
ALTER TABLE `activites`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_apprenant` (`id_apprenant`);

--
-- Index pour la table `cours`
--
ALTER TABLE `cours`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_formateur` (`id_formateur`);

--
-- Index pour la table `fiches_journalieres`
--
ALTER TABLE `fiches_journalieres`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_formateur` (`id_formateur`);

--
-- Index pour la table `parcours`
--
ALTER TABLE `parcours`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `quizz`
--
ALTER TABLE `quizz`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_cours` (`id_cours`);

--
-- Index pour la table `resultats_quizz`
--
ALTER TABLE `resultats_quizz`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_apprenant` (`id_apprenant`),
  ADD KEY `id_quizz` (`id_quizz`);

--
-- Index pour la table `utilisateurs`
--
ALTER TABLE `utilisateurs`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `id_parcours` (`id_parcours`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `activites`
--
ALTER TABLE `activites`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `cours`
--
ALTER TABLE `cours`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `fiches_journalieres`
--
ALTER TABLE `fiches_journalieres`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `parcours`
--
ALTER TABLE `parcours`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `quizz`
--
ALTER TABLE `quizz`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `resultats_quizz`
--
ALTER TABLE `resultats_quizz`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `utilisateurs`
--
ALTER TABLE `utilisateurs`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `activites`
--
ALTER TABLE `activites`
  ADD CONSTRAINT `activites_ibfk_1` FOREIGN KEY (`id_apprenant`) REFERENCES `utilisateurs` (`id`);

--
-- Contraintes pour la table `cours`
--
ALTER TABLE `cours`
  ADD CONSTRAINT `cours_ibfk_1` FOREIGN KEY (`id_formateur`) REFERENCES `utilisateurs` (`id`);

--
-- Contraintes pour la table `fiches_journalieres`
--
ALTER TABLE `fiches_journalieres`
  ADD CONSTRAINT `fiches_journalieres_ibfk_1` FOREIGN KEY (`id_formateur`) REFERENCES `utilisateurs` (`id`);

--
-- Contraintes pour la table `quizz`
--
ALTER TABLE `quizz`
  ADD CONSTRAINT `quizz_ibfk_1` FOREIGN KEY (`id_cours`) REFERENCES `cours` (`id`);

--
-- Contraintes pour la table `resultats_quizz`
--
ALTER TABLE `resultats_quizz`
  ADD CONSTRAINT `resultats_quizz_ibfk_1` FOREIGN KEY (`id_apprenant`) REFERENCES `utilisateurs` (`id`),
  ADD CONSTRAINT `resultats_quizz_ibfk_2` FOREIGN KEY (`id_quizz`) REFERENCES `quizz` (`id`);

--
-- Contraintes pour la table `utilisateurs`
--
ALTER TABLE `utilisateurs`
  ADD CONSTRAINT `utilisateurs_ibfk_1` FOREIGN KEY (`id_parcours`) REFERENCES `parcours` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
