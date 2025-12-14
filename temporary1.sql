-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 14, 2025 at 04:59 PM
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
-- Database: `temporary1`
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
('R6', 'n xx', 'zXZX', 'ZXZX', '2025-12-17', 12, 'Female', 'SDNJASND', 'Single', 'ASDASDAS', 'ASDASD', 'jsanda', 'HH1'),
('R7', 'n xx', 'zXZX', 'ZXZX', '2025-12-17', 12, 'Male', 'SDNJASND', 'Married', 'ASDASDAS', 'ASDASD', 'jsanda', 'HH3'),
('R8', 'n xx', 'zXZX', 'ZXZX', '2025-12-17', 12, 'Male', 'SDNJASND', 'Single', 'ASDASDAS', 'ASDASD', 'jsanda', 'HH1'),
('R9', 'n xx', 'zXZX', 'ZXZX', '2025-12-17', 12, 'Male', 'SDNJASND', 'Single', 'ASDASDAS', 'ASDASD', 'jsanda', 'HH4'),
('R10', 'n xx', 'zXZX', 'assa', '2025-12-20', 12, 'Male', 'SDNJASND', 'Single', 'ASDASDAS', 'ASDASD', 'jsanda', 'HH5'),
('R10', 'n xx', 'zXZX', 'assa', '2025-12-20', 12, 'Male', 'SDNJASND', 'Married', 'ASDASDAS', 'ASDASD', 'jsanda', 'HH5'),
('R10', 'n xx', 'zXZX', 'assa', '2026-01-01', 12, 'Male', 'SDNJASND', 'Single', 'ASDASDAS', 'ASDASD', 'jsanda', 'HH5'),
('R10', 'n xx', 'zXZX', 'ZXZX', '2025-12-17', 12, 'Male', 'SDNJASND', 'Single', 'ASDASDAS', 'ASDASD', 'jsanda', 'HH5'),
('R10', 'n xx', 'zXZX', 'ZXZX', '2025-12-17', 12, 'Female', 'SDNJASND', 'Single', 'ASDASDAS', 'ASDASD', 'jsanda', 'HH5'),
('R10', 'n xx', 'zXZX', 'ZXZX', '2025-12-17', 12, 'Male', 'SDNJASND', 'Single', 'ASDASDAS', 'ASDASD', 'jsanda', 'HH5'),
('R011', 'n xx', 'zXZX', 'ZXZX', '2025-12-17', 12, 'Male', 'SDNJASND', 'Married', 'ASDASDAS', 'ASDASD', 'jsanda', 'HH6'),
('R012', 'n xx', 'zXZX', 'ZXZX', '2025-12-17', 12, 'Male', 'SDNJASND', 'Single', 'ASDASDAS', 'ASDASD', 'jsanda', 'HH6'),
('R013', 'n xx', 'zXZX', 'assa', '2026-01-01', 12, 'Male', 'SDNJASND', 'Single', 'ASDASDAS', 'ASDASD', 'jsanda', 'HH7'),
('R014', 'n xx', 'zXZX', 'assa', '2026-01-01', 12, 'Male', 'SDNJASND', 'Single', 'ASDASDAS', 'ASDASD', 'jsanda', 'None');

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
('HOW', 'AS', 'DS', 'SA', '12345'),
('willcor', 'as', 'askmasd', 'willcor', '12345'),
('cals', 'jnsd', 'asd', 'asd', 'asd'),
('jn', 'jnk', 'k', 'lk', 'jn'),
('aBSJ', 'SADBJAS', 'SABD', 'SAJD', 'ASJDN'),
('kasjdk', 'jsandas', 'jasnd', 'jsand', 'jsandn'),
('hjhjkjk', 'hbbjb', 'hbb', 'hbhb', 'hbhb');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
