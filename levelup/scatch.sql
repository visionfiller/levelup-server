SELECT a.first_name,a.last_name, e.*, lg.title
FROM levelupapi_event e
JOIN levelupapi_gamer g ON e.organizer_id = g.id
JOIN auth_user a ON a.id = g.user_id
JOIN levelupapi_game lg ON lg.id = e.game_id
          