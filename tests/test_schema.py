import sqlite3
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
H1 = '8cbef1c2-3469-4e81-9ff1-5bfa1dc80001'
H2 = '8cbef1c2-3469-4e81-9ff1-5bfa1dc80002'

class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        self.db.executescript((ROOT / 'database/schema.sql').read_text())
        self.db.executescript((ROOT / 'database/seed_data.sql').read_text())

    def tearDown(self):
        self.db.close()

    def test_seed_and_monthly_example(self):
        count = self.db.execute('SELECT COUNT(*) FROM completions WHERE habit_id=? AND completion_date BETWEEN ? AND ?', (H1, '2026-10-01', '2026-10-20')).fetchone()[0]
        self.assertEqual((count, round(count / 20 * 100)), (12, 60))
        self.assertEqual(self.db.execute('PRAGMA foreign_key_check').fetchall(), [])
        self.assertEqual(self.db.execute('PRAGMA integrity_check').fetchone()[0], 'ok')

    def test_title_description_and_date_validation(self):
        for title, description, date in [(' \t\n', None, '2026-10-01'), ('x' * 101, None, '2026-10-01'), ('ok', 'x' * 501, '2026-10-01'), ('ok', None, '2026-02-30'), ('ok', None, 'bad')]:
            with self.subTest(title=title, date=date), self.assertRaises(sqlite3.IntegrityError):
                self.db.execute('INSERT INTO habits VALUES (?, ?, ?, ?)', ('new', title, description, date))
        self.db.execute('INSERT INTO habits VALUES (?, ?, ?, ?)', ('valid', 'x' * 100, 'x' * 500, '2024-02-29'))

    def test_duplicate_and_orphan_rejected(self):
        for args in [(H1, '2026-10-01'), ('missing', '2026-10-15')]:
            with self.subTest(args=args), self.assertRaises(sqlite3.IntegrityError):
                self.db.execute('INSERT INTO completions VALUES (?, ?)', args)

    def test_idempotent_insert(self):
        self.db.execute('INSERT INTO completions VALUES (?, ?) ON CONFLICT(habit_id, completion_date) DO NOTHING', (H1, '2026-10-01'))
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM completions WHERE habit_id=? AND completion_date=?', (H1, '2026-10-01')).fetchone()[0], 1)

    def test_completion_date_constraints_on_insert_and_update(self):
        for date in ('2026-10-09', '2026-02-30', 'bad'):
            with self.subTest(date=date), self.assertRaises(sqlite3.IntegrityError):
                self.db.execute('INSERT INTO completions VALUES (?, ?)', (H2, date))
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute('UPDATE completions SET completion_date=? WHERE habit_id=? AND completion_date=?', ('2026-10-09', H2, '2026-10-10'))
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute('UPDATE habits SET created_date=? WHERE habit_id=?', ('2026-10-15', H2))

    def test_delete_cascades_only_related_completions(self):
        self.db.execute('DELETE FROM habits WHERE habit_id=?', (H2,))
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM completions WHERE habit_id=?', (H2,)).fetchone()[0], 0)
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM completions WHERE habit_id=?', (H1,)).fetchone()[0], 12)

if __name__ == '__main__':
    unittest.main(verbosity=2)
