INSERT INTO bitcoin (timestamp, open, high, low, close, volume, number_of_trades)
VALUES
('2024-12-27 10:00:00', 50000.00, 51000.00, 49500.00, 50500.00, 120.5, 300),
('2024-12-27 11:00:00', 50500.00, 51500.00, 50000.00, 51000.00, 130.7, 320)
ON CONFLICT (timestamp) DO NOTHING;
 
INSERT INTO ethereum (timestamp, open, high, low, close, volume, number_of_trades)
VALUES
('2024-12-27 10:00:00', 4000.00, 4100.00, 3950.00, 4050.00, 75.3, 210),
('2024-12-27 11:00:00', 4050.00, 4150.00, 4000.00, 4100.00, 80.4, 220)
ON CONFLICT (timestamp) DO NOTHING;

INSERT INTO binance (timestamp, open, high, low, close, volume, number_of_trades)
VALUES
('2024-12-27 10:00:00', 300.00, 310.00, 295.00, 305.00, 50.2, 100),
('2024-12-27 11:00:00', 305.00, 315.00, 300.00, 310.00, 55.1, 110)
ON CONFLICT (timestamp) DO NOTHING;

INSERT INTO solana (timestamp, open, high, low, close, volume, number_of_trades)
VALUES
('2024-12-27 10:00:00', 20.00, 21.00, 19.50, 20.50, 15.6, 50),
('2024-12-27 11:00:00', 20.50, 21.50, 20.00, 21.00, 16.2, 55)
ON CONFLICT (timestamp) DO NOTHING;