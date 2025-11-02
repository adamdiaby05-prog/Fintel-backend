-- Migration pour changer profile_picture_url de VARCHAR(500) à TEXT
-- pour supporter les images base64 qui peuvent être très longues

ALTER TABLE users 
ALTER COLUMN profile_picture_url TYPE TEXT;

