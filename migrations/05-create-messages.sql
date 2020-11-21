CREATE TABLE messages(
    id INT NOT NULL AUTO_INCREMENT,
	chat_id INT NOT NULL,
    login VARCHAR(60) NOT NULL,
    message TEXT NOT NULL,
	PRIMARY KEY (id),
    FOREIGN KEY (chat_id)
        REFERENCES chats (id)
        ON DELETE CASCADE,
    FOREIGN KEY (login)
        REFERENCES users (login)
);