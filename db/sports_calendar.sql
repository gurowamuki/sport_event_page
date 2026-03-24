DROP TABLE IF EXISTS event_result CASCADE;
DROP TABLE IF EXISTS event CASCADE;
DROP TABLE IF EXISTS team CASCADE;
DROP TABLE IF EXISTS venue CASCADE;
DROP TABLE IF EXISTS city CASCADE;
DROP TABLE IF EXISTS country CASCADE;
DROP TABLE IF EXISTS sport CASCADE;

CREATE TABLE country (
    country_id SERIAL PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL UNIQUE,
    code CHAR(3) NOT NULL UNIQUE   
);

CREATE TABLE city (
    city_id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    _country_id  INTEGER NOT NULL REFERENCES country(country_id),
    UNIQUE (city_name, _country_id)
);

CREATE TABLE venue (
    venue_id SERIAL PRIMARY KEY,
    venue_name VARCHAR(150) NOT NULL,
    venue_address VARCHAR(255),
    capacity INTEGER CHECK (capacity > 0),
    _city_id INTEGER NOT NULL REFERENCES city(city_id)
);

CREATE TABLE sport (
    sport_id SERIAL PRIMARY KEY,
    sport_name VARCHAR(100) NOT NULL UNIQUE,
    sport_description TEXT
);

CREATE TABLE league (
    league_id SERIAL PRIMARY KEY,
    league_name VARCHAR(150) NOT NULL,
    season VARCHAR(20),
    _sport_id INTEGER NOT NULL REFERENCES sport(sport_id),
    _country_id INTEGER REFERENCES country(country_id),          
    UNIQUE (league_name, season)
);

CREATE TABLE team (
    team_id SERIAL PRIMARY KEY,
    team_name VARCHAR(150) NOT NULL,
    short_name VARCHAR(10),          
    founded_year INTEGER,
    _sport_id INTEGER NOT NULL REFERENCES sport(sport_id),
    _city_id INTEGER REFERENCES city(city_id),
    UNIQUE (team_name, _sport_id)
);

CREATE TABLE event (
    event_id SERIAL PRIMARY KEY,
    event_date DATE NOT NULL,
    event_time TIME NOT NULL,
    _sport_id INTEGER NOT NULL REFERENCES sport(sport_id),
    _league_id INTEGER REFERENCES league(league_id),
    _venue_id INTEGER REFERENCES venue(venue_id),
    _home_team_id INTEGER NOT NULL REFERENCES team(team_id),
    _away_team_id INTEGER NOT NULL REFERENCES team(team_id),
    event_description TEXT,
    event_status VARCHAR(20) NOT NULL DEFAULT 'scheduled' CHECK (event_status IN ('scheduled', 'live', 'finished', 'postponed', 'cancelled')),
    CONSTRAINT different_teams CHECK (_home_team_id <> _away_team_id)
);

CREATE TABLE event_result (
    result_id SERIAL PRIMARY KEY,
    _event_id INTEGER  NOT NULL UNIQUE REFERENCES event(event_id),
    home_score INTEGER NOT NULL CHECK (home_score >= 0),
    away_score INTEGER NOT NULL CHECK (away_score >= 0),
    notes TEXT            
);

-- ============================================================

INSERT INTO country (country_name, code) VALUES
    ('Austria', 'AUT'),
    ('Germany', 'DEU'),
    ('United Kingdom', 'GBR');

INSERT INTO city (city_name, _country_id) VALUES
    ('Salzburg', (SELECT country_id FROM country WHERE code = 'AUT')),
    ('Vienna', (SELECT country_id FROM country WHERE code = 'AUT')),
    ('Graz', (SELECT country_id FROM country WHERE code = 'AUT')),
    ('Klagenfurt', (SELECT country_id FROM country WHERE code = 'AUT')),
    ('Munich', (SELECT country_id FROM country WHERE code = 'DEU')),
    ('London', (SELECT country_id FROM country WHERE code = 'GBR'));

INSERT INTO venue (venue_name, venue_address, capacity, _city_id) VALUES
    ('Red Bull Arena', 'Am Bullevard 1, Salzburg', 30188, (SELECT city_id FROM city WHERE city_name = 'Salzburg')),
    ('Merkur Arena', 'Liebenauer Hauptstr. 317', 16364, (SELECT city_id FROM city WHERE city_name = 'Graz')),
    ('Stadthalle Vienna', 'Roland-Rainer-Platz 1', 16000, (SELECT city_id FROM city WHERE city_name = 'Vienna')),
    ('Klagenfurt Arena', 'Stadtring 1, Klagenfurt', 7200, (SELECT city_id FROM city WHERE city_name = 'Klagenfurt')),
    ('Allianz Arena', 'Werner-Heisenberg-Allee 25', 75000, (SELECT city_id FROM city WHERE city_name = 'Munich')),
    ('Wembley Stadium', 'London HA9 0WS', 90000, (SELECT city_id FROM city WHERE city_name = 'London'));
  
INSERT INTO sport (sport_name, sport_description) VALUES
    ('Football', 'Association football, also known as soccer'),
    ('Ice Hockey', 'Team sport played on ice with sticks and a puck'),
    ('Basketball', 'Team sport played on a court with a ball and hoops');
 
INSERT INTO league (league_name, season, _sport_id, _country_id) VALUES
    ('Austrian Bundesliga',
        '2019/2020',
        (SELECT sport_id FROM sport WHERE sport_name = 'Football'),
        (SELECT country_id FROM country WHERE code = 'AUT')),
    ('EBEL Ice Hockey',
        '2019/2020',
        (SELECT sport_id FROM sport WHERE sport_name = 'Ice Hockey'),
        (SELECT country_id FROM country WHERE code = 'AUT')),
    ('Austrian Basketball League',
        '2019/2020',
        (SELECT sport_id FROM sport WHERE sport_name = 'Basketball'),
        (SELECT country_id FROM country WHERE code = 'AUT')),
    ('Bundesliga',
        '2019/2020',
        (SELECT sport_id FROM sport WHERE sport_name = 'Football'),
        (SELECT country_id FROM country WHERE code = 'DEU')),
    ('Premier League',
        '2019/2020',
        (SELECT sport_id FROM sport WHERE sport_name = 'Football'),
        (SELECT country_id FROM country WHERE code = 'GBR'));

INSERT INTO team (team_name, short_name, founded_year, _sport_id, _city_id) VALUES
    ('FC Red Bull Salzburg', 'SAL', 1933,
        (SELECT sport_id FROM sport WHERE sport_name = 'Football'),
        (SELECT city_id FROM city WHERE city_name = 'Salzburg')),
    ('SK Sturm Graz', 'STU', 1909,
        (SELECT sport_id FROM sport WHERE sport_name = 'Football'),
        (SELECT city_id FROM city WHERE city_name = 'Graz')),
    ('SK Rapid Vienna', 'RAP', 1899,
        (SELECT sport_id FROM sport WHERE sport_name = 'Football'),
        (SELECT city_id FROM city WHERE city_name = 'Vienna')),
    ('FK Austria Vienna', 'AUS', 1911,
        (SELECT sport_id FROM sport WHERE sport_name = 'Football'),
        (SELECT city_id FROM city WHERE city_name = 'Vienna')), 
    ('FC Bayern Munich', 'BAY', 1900,
        (SELECT sport_id FROM sport WHERE sport_name = 'Football'),
        (SELECT city_id FROM city WHERE city_name = 'Munich')),
 
    ('EC KAC', 'KAC', 1909,
        (SELECT sport_id FROM sport WHERE sport_name = 'Ice Hockey'),
        (SELECT city_id FROM city WHERE city_name = 'Klagenfurt')),
 
    ('Vienna Capitals', 'CAP', 1999,
        (SELECT sport_id FROM sport WHERE sport_name = 'Ice Hockey'),
        (SELECT city_id FROM city WHERE city_name = 'Vienna')),
 
    ('EC Red Bull Salzburg', 'RBS', 2000,
        (SELECT sport_id FROM sport WHERE sport_name = 'Ice Hockey'),
        (SELECT city_id FROM city WHERE city_name = 'Salzburg'));
 
INSERT INTO event (event_date, event_time, _sport_id, _league_id, _venue_id, _home_team_id, _away_team_id, event_description, event_status) VALUES
    ('2026-07-18', '18:30',
        (SELECT sport_id FROM sport WHERE sport_name = 'Football'),
        (SELECT league_id FROM league WHERE league_name = 'Austrian Bundesliga'),
        (SELECT venue_id FROM venue WHERE venue_name = 'Red Bull Arena'),
        (SELECT team_id FROM team WHERE team_name = 'FC Red Bull Salzburg'),
        (SELECT team_id FROM team WHERE team_name = 'SK Sturm Graz'),
        'Austrian Bundesliga matchday 3', 'scheduled'),
    ('2026-10-23', '09:45',
        (SELECT sport_id FROM sport WHERE sport_name = 'Ice Hockey'),
        (SELECT league_id FROM league WHERE league_name = 'EBEL Ice Hockey'),
        (SELECT venue_id FROM venue WHERE venue_name = 'Klagenfurt Arena'),
        (SELECT team_id FROM team WHERE team_name = 'EC KAC'),
        (SELECT team_id FROM team WHERE team_name = 'Vienna Capitals'),
        'EBEL regular season game', 'scheduled'),
    ('2026-11-02', '16:00',
        (SELECT sport_id FROM sport WHERE sport_name = 'Football'),
        (SELECT league_id FROM league WHERE league_name = 'Austrian Bundesliga'),
        (SELECT venue_id FROM venue WHERE venue_name = 'Merkur Arena'),
        (SELECT team_id FROM team WHERE team_name = 'SK Sturm Graz'),
        (SELECT team_id FROM team WHERE team_name = 'SK Rapid Vienna'),
        'Austrian Bundesliga matchday 12', 'scheduled'),
    ('2026-12-07', '18:30',
        (SELECT sport_id FROM sport WHERE sport_name = 'Football'),
        (SELECT league_id FROM league WHERE league_name = 'Austrian Bundesliga'),
        (SELECT venue_id FROM venue WHERE venue_name = 'Red Bull Arena'),
        (SELECT team_id FROM team WHERE team_name = 'FC Red Bull Salzburg'),
        (SELECT team_id FROM team WHERE team_name = 'FK Austria Vienna'),
        'Austrian Bundesliga matchday 18', 'scheduled'),
    ('2026-01-15', '19:15',
        (SELECT sport_id FROM sport WHERE sport_name = 'Ice Hockey'),
        (SELECT league_id FROM league WHERE league_name = 'EBEL Ice Hockey'),
        (SELECT venue_id FROM venue WHERE venue_name = 'Stadthalle Vienna'),
        (SELECT team_id FROM team WHERE team_name = 'Vienna Capitals'),
        (SELECT team_id FROM team WHERE team_name = 'EC KAC'),
        'EBEL regular season game', 'finished'), 
    ('2026-02-08', '15:30',
        (SELECT sport_id FROM sport WHERE sport_name = 'Ice Hockey'),
        (SELECT league_id FROM league WHERE league_name = 'EBEL Ice Hockey'),
        (SELECT venue_id FROM venue WHERE venue_name = 'Red Bull Arena'),
        (SELECT team_id FROM team WHERE team_name = 'EC Red Bull Salzburg'),
        (SELECT team_id FROM team WHERE team_name = 'EC KAC'),
        'EBEL regular season game', 'postponed'),
    ('2026-03-01', '14:00',
        (SELECT sport_id FROM sport WHERE sport_name = 'Football'),
        (SELECT league_id FROM league WHERE league_name = 'Austrian Bundesliga'),
        (SELECT venue_id FROM venue WHERE venue_name = 'Stadthalle Vienna'),
        (SELECT team_id FROM team WHERE team_name = 'SK Rapid Vienna'),
        (SELECT team_id FROM team WHERE team_name = 'FK Austria Vienna'),
        'Vienna derby matchday 24', 'cancelled');
 
INSERT INTO event_result (_event_id, home_score, away_score, notes) VALUES
    ((SELECT event_id FROM event WHERE event_date = '2026-07-18'), 3, 1, NULL),
    ((SELECT event_id FROM event WHERE event_date = '2026-10-23'), 4, 2, NULL),
    ((SELECT event_id FROM event WHERE event_date = '2026-11-02'), 2, 2, 'AET');