from task import Task


class CalendarTask(Task):

    def get_houses(self):
        sql = "SELECT house_id FROM houses"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def run(self):
        houses = self.get_houses()
        self.logger.info("Create calendar tasks of %s houses." % (str(len(houses)),))
        for h in houses:
            try:
                self.redis.lpush("calendar:start_urls", h['house_id'])
            except Exception as e:
                self.logger.exception(e)
                # TODO: send message


if __name__ == "__main__":
    task = CalendarTask()
    task.run()


    