-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Anamakine: 127.0.0.1
-- Üretim Zamanı: 26 Ara 2020, 21:50:32
-- Sunucu sürümü: 10.4.14-MariaDB
-- PHP Sürümü: 7.4.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `url_hunter`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `companys`
--

CREATE TABLE `companys` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `description` text NOT NULL,
  `url` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `links`
--

CREATE TABLE `links` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `description` text NOT NULL,
  `arg` text NOT NULL,
  `company` int(11) NOT NULL,
  `domain` text NOT NULL,
  `short_name` text NOT NULL,
  `priv` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Tablo döküm verisi `links`
--

INSERT INTO `links` (`id`, `name`, `description`, `arg`, `company`, `domain`, `short_name`, `priv`) VALUES
(1, 'Ay link', 'trlink adlı link kısaltma sitesine ait bir alan adıdır. (default olarak kısa linkleri bu alan adına verir)', 'aylink', 1, 'aylink.co', 'aylink', 1),
(2, 'Yindex', 'tr.link adlı link kısaltma sitesine ait bir alan adıdır.', 'yindex', 1, 'yindex.xyz', 'yindex', 1),
(3, 'Git izle', 'tr.link adlı link kısaltma sitesine ait bir alan adıdır.', 'gitizle', 1, 'gitizle.vip', 'gitizle', 1),
(4, 'Ekitap-indir', 'tr.link adlı link kısaltma sitesine ait bir alan adıdır.', 'ekitap-indir', 1, 'ekitap-indir.net', 'ekitap-indir', 1),
(5, 'Son dakika', 'tr.link adlı link kısaltma sitesine ait bir alan adıdır.', 'sondakika', 1, 'sondakika.pro', 'sondakika', 1),
(6, 'İndir torrent', 'tr.link adlı link kısaltma sitesine ait bir alan adıdır.', 'indirtorrent', 1, 'indir-torrent.xyz', 'indir-torrent', 1),
(7, 'Open load', 'tr.link adlı link kısaltma sitesine ait bir alan adıdır.', 'openload', 1, 'openload.red', 'openload', 1),
(8, 'Tam indir', 'tr.link adlı link kısaltma sitesine ait bir alan adıdır.', 'tamindir', 1, 'tamindir.mobi', 'tamindir', 1),
(9, 'Uzun versiyon', 'tr.link adlı link kısaltma sitesine ait bir alan adıdır.', 'uzunversiyon', 1, 'uzunversiyon.co', 'uzunversiyon', 1),
(10, 'Sht', 'tr.link adlı link kısaltma sitesine ait bir alan adıdır.', 'sht', 1, 'sht.ms', 'sht', 1),
(11, 'OuO', 'Bu Site, yayıncıların herhangi bir URL\'yi kısaltmasına ve kısaltılmış URL\'yi paylaşarak gelir elde etmesine olanak tanır.', 'ouo', 2, 'ouo.io', 'ouo', 0),
(12, 'Met', 'met.bz - URL kısaltıcı, kısa bağlantılar oluşturabileceğiniz ücretsiz bir çevrimiçi araçtır, ödeme alırsınız! Bağlantılarınızı yönetirken evden para kazanabilirsiniz.', 'met', 3, 'met.bz', 'met', 0),
(13, 'Findi', 'tr.link adlı link kısaltma sitesine ait bir alan adıdır. Geçilnmesi imkansızdır yalnızca para kazandırır.', 'findi', 1, 'findi.pro', 'findi', 1);
-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `ticket`
--

CREATE TABLE `ticket` (
  `id` int(11) NOT NULL,
  `user` int(11) NOT NULL,
  `supporter` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `message` text NOT NULL,
  `response` text NOT NULL,
  `created_date` text NOT NULL,
  `finish_date` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `transactions`
--

CREATE TABLE `transactions` (
  `id` int(11) NOT NULL,
  `user` int(11) NOT NULL,
  `company` int(11) NOT NULL,
  `link` text NOT NULL,
  `short_url` text NOT NULL,
  `finish_url` text NOT NULL,
  `date` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `d_id` text NOT NULL,
  `reg_date` text NOT NULL,
  `priv` int(11) NOT NULL,
  `skipped_links` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dökümü yapılmış tablolar için indeksler
--

--
-- Tablo için indeksler `companys`
--
ALTER TABLE `companys`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `links`
--
ALTER TABLE `links`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Dökümü yapılmış tablolar için AUTO_INCREMENT değeri
--

--
-- Tablo için AUTO_INCREMENT değeri `companys`
--
ALTER TABLE `companys`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Tablo için AUTO_INCREMENT değeri `links`
--
ALTER TABLE `links`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Tablo için AUTO_INCREMENT değeri `ticket`
--
ALTER TABLE `ticket`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Tablo için AUTO_INCREMENT değeri `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Tablo için AUTO_INCREMENT değeri `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
