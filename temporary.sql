-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 12, 2025 at 03:38 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `temporary`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `RefId` text NOT NULL,
  `Name` text NOT NULL,
  `MI` text NOT NULL,
  `LastName` text NOT NULL,
  `Birthday` date NOT NULL,
  `Age` int(11) NOT NULL,
  `Sex` text NOT NULL,
  `Address` text NOT NULL,
  `CivilStatus` text NOT NULL,
  `Occupation` text NOT NULL,
  `Nationality` text NOT NULL,
  `Zone` text NOT NULL,
  `HouseholdID` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`RefId`, `Name`, `MI`, `LastName`, `Birthday`, `Age`, `Sex`, `Address`, `CivilStatus`, `Occupation`, `Nationality`, `Zone`, `HouseholdID`) VALUES
('R1', 'ronel', 'knksdkansd', 'sjakndkkas', '0000-00-00', 23, 'Male', 'SDNJASND', 'Single', 'ASDASDAS', 'filipino', 'sandkas', 'HH1'),
('R3', 'nmnkm', 'sada', 'sjakndkkas', '2025-12-16', 23, 'Male', 'SDNJASND', 'Single', 'ASDASDAS', 'filipino', 'sandkas', 'HH1'),
('R4', 'jnnlm', 'sada', 'sjakndkkas', '2025-12-16', 23, 'Female', 'SDNJASND', 'Single', 'ASDASDAS', 'filipino', 'sandkas', 'HH4'),
('R5', 'kadkasd', 'sada', 'sjakndkkas', '2025-12-16', 23, 'Male', 'SDNJASND', 'Single', 'ASDASDAS', 'filipino', 'sandkas', 'HH3'),
('R6', 'jbjknnkn', 'sada', 'sjakndkkas', '2025-12-16', 23, 'Male', 'SDNJASND', 'Married', 'ASDASDAS', 'filipino', 'koakd', 'HH5'),
('R7', 'jnlkmlm', 'jNZX', 'sjakndkkas', '2025-12-16', 23, 'Male', 'SDNJASND', 'Single', 'ASDASDAS', 'filipino', 'nm.m,', 'HH6'),
('R8', 'sjakndkkas', 'as', 'sjakndkkas', '2025-12-10', 88, 'Male', 'SDNJASND', 'Single', 'ASDASDAS', 'ASDASD', 'zone 1', 'HH7');

-- --------------------------------------------------------

--
-- Table structure for table `adminacc`
--

CREATE TABLE `adminacc` (
  `Username` text NOT NULL,
  `Password` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `adminacc`
--

INSERT INTO `adminacc` (`Username`, `Password`) VALUES
('admin', 'admin123');

-- --------------------------------------------------------

--
-- Table structure for table `useracc`
--

CREATE TABLE `useracc` (
  `FirstName` text NOT NULL,
  `MiddleName` text NOT NULL,
  `LastName` text NOT NULL,
  `Username` text NOT NULL,
  `Password` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `useracc`
--

INSERT INTO `useracc` (`FirstName`, `MiddleName`, `LastName`, `Username`, `Password`) VALUES
('ronell', 'asa', 'assa', 'user', '12345'),
('willcor', 'as', 'askmasd', 'willcor', '12345');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
