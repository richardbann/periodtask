periodtask
==========

.. image:: https://travis-ci.org/vertisfinance/periodtask.svg?branch=master
  :target: https://travis-ci.org/vertisfinance/periodtask

.. image:: https://coveralls.io/repos/github/vertisfinance/periodtask/badge.svg?branch=master
  :target: https://coveralls.io/github/vertisfinance/periodtask?branch=master

Periodic task with timezone

.. code-block:: python

  #!/usr/bin/env python3

  import logging
  import os

  from periodtask import TaskList, Task
  from periodtask.mailsender import MailSender


  logging.basicConfig(level=logging.INFO)

  send_success = MailSender(
      os.environ.get('EMAIL_HOST'),
      int(os.environ.get('EMAIL_PORT')),
      os.environ.get('EMAIL_FROM'),
      os.environ.get('EMAIL_RECIPIENT'),
  ).send_mail

  tasks = TaskList(
      Task(
          name='test',
          command=('ls', '-al'),
          periods='* * * * * Europe/Budapest * 0',
          run_on_start=True,
          mail_success=True,
          send_mail_func=send_success,
      ),
      Task(
          name='test',
          command=('cat', 'README.rst'),
          periods='* * * * * Europe/Budapest * 0',
          run_on_start=True,
          mail_success=send_success,
      )
  )

  tasks.start()
