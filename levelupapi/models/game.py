from django.db import models


class Game(models.Model):
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE, related_name='games')
    gamer = models.ForeignKey("Gamer", null=True, blank=True, on_delete=models.CASCADE, related_name='games')
    title = models.CharField(max_length=155)
    maker = models.CharField(max_length=155)
    number_of_players = models.IntegerField()
    skill_level = models.IntegerField()
    