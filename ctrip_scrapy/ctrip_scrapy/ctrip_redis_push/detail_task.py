from task import Task


class DetailTask(Task):

    def get_houses(self):
        # sql = "SELECT hp.house_id, hdr.create_time FROM houses hp LEFT JOIN house_detail_response hdr " \
        #       "ON hp.house_id=hdr.house_id WHERE hdr.create_time IS NULL"
        sql = "SELECT house_id FROM houses WHERE detail_crawled=0"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def run(self):
        houses = self.get_houses()
        self.logger.info("Create detail tasks of %s houses." % (str(len(houses)), ))
        for h in houses:
            try:
                self.redis.lpush("detail:start_urls", h['house_id'])
            except Exception as e:
                self.logger.exception(e)
                # TODO: send message


if __name__ == "__main__":
    task = DetailTask()
    task.run()


    