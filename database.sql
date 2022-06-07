USE `ordenes`;

DELETE FROM `customer`;
INSERT INTO `customer` (`customer_id`, `name`, `email`) VALUES
	(1, 'mauricio', 'mauricio@gmail.com'),
	(2, 'jose', 'jose@gmail.com'),
	(3, 'marcelo', 'marcelo@gmail.com'),
	(4, 'carlos', 'carlos@gmail.com'),
	(5, 'esteban', 'esteban@gmail.com'),
	(6, 'johan', 'johan@gmail.com'),
	(7, 'carolina', 'carolina@gmail.com'),
	(8, 'carmen', 'carmen@gmail.com');



-- Volcando datos para la tabla ordenes.customer_has_product: ~11 rows (aproximadamente)
DELETE FROM `customer_has_product`;
INSERT INTO `customer_has_product` (`customer_id`, `product_id`) VALUES
	(1, 1),
	(1, 2),
	(1, 6),
	(4, 4),
	(4, 5),
	(2, 5),
	(1, 4),
	(1, 3),
	(1, 5),
	(3, 5),
	(3, 1),
	(5, 1),
	(5, 2),
	(5, 3),
	(5, 4),
	(5, 5),
	(5, 6),
	(5, 7),
	(5, 8),
	(6, 5),
	(6, 1),
	(7, 9),
	(7, 7),
	(7, 6),
	(8, 4);






-- Volcando datos para la tabla ordenes.product: ~9 rows (aproximadamente)
DELETE FROM `product`;
INSERT INTO `product` (`product_id`, `name`, `description`, `price`) VALUES
	(1, 'mesa', 'mesa de madera', 12.5),
	(2, 'silla', 'silla de madera', 9.58),
	(3, 'mesedora', 'mesedora metalica', 19.8),
	(4, 'cama ', 'cama detalica', 50.2),
	(5, 'mesa de noche', 'mesa de noche en madera', 25.6),
	(6, 'portatil', 'portatil hp', 500.5),
	(7, 'table', 'table samsung', 200.9),
	(8, 'celular', 'celular huawei', 580.8),
	(9, 'escritorio', 'escritorio en madera y metal', 150.7);


