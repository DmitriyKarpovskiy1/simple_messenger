CREATE TABLE chats_users_notifications(
	chat_id INT NOT NULL,
    login VARCHAR(60) NOT NULL,
	CONSTRAINT chat_id_login PRIMARY KEY (chat_id, login),
    FOREIGN KEY (chat_id)
        REFERENCES chats (id)
        ON DELETE CASCADE,
    FOREIGN KEY (login)
        REFERENCES users (login)
);
