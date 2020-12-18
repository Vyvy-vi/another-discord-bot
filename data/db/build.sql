CREATE TABLE IF NOT EXISTS guilds(
    GuildID TEXT PRIMARY KEY,
    Prefix TEXT DEFAULT "."
);

CREATE TABLE IF NOT EXISTS exp (
    UserId TEXT PRIMARY KEY,
    XP BIGINT DEFAULT 0,
    Level integer DEFAULT 0,
    XPLock text DEFAULT CURRENT_TIMESTAMP
);
