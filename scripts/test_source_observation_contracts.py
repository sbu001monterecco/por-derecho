from html.parser import HTMLParser
import hashlib,json
from pathlib import Path
import subprocess,tempfile,unittest
from source_observation_contracts import preserved_owned_page,find_frozen_origin

class OwnedTests(unittest.TestCase):
 def expected(self):return '<main>Prior evidence.<section id="owned"><div>Distinct but interconnected.</div><p>Not liability by association.</p></section></main>'
 def check(self,actual):preserved_owned_page('fixture',self.expected(),actual,'owned')
 def test_independent_addition_allowed(self):self.check(self.expected().replace('</main>','<section>New reader link.</section></main>'))
 def test_controlled_text_rewrite_fails(self):
  with self.assertRaises(AssertionError):self.check(self.expected().replace('Distinct','Independent'))
 def test_old_text_deletion_fails(self):
  with self.assertRaises(AssertionError):self.check(self.expected().replace('Prior evidence.',''))
 def test_duplicate_control_fails(self):
  with self.assertRaises(AssertionError):self.check(self.expected()+self.expected())
 def test_missing_control_fails(self):
  with self.assertRaises(AssertionError):self.check('<main>Prior evidence.</main>')
 def test_nested_elements_not_truncated(self):
  with self.assertRaises(AssertionError):self.check(self.expected().replace('Not liability','Automatic liability'))

class Parser(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.inline_identity_markup=[]
 def handle_data(self,data):self.parts.append(data)

class HistoricalTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
  def git(*args):return subprocess.check_output(['git',*args],cwd=self.root,stderr=subprocess.DEVNULL).decode().strip()
  self.git=git;git('init','-q');git('config','user.name','Fixture');git('config','user.email','fixture@example.invalid')
  self.control={'rendered_occurrence_control':{'route_snapshots':[]}}
  for i in range(18):
   path=self.root/f'p{i}/index.html';path.parent.mkdir();path.write_text(f'<main>Historical {i}</main>');t=f'Historical {i}'
   self.control['rendered_occurrence_control']['route_snapshots'].append({'route':f'/p{i}/','normalized_characters':len(t),'normalized_main_sha256':hashlib.sha256(t.encode()).hexdigest()})
  (self.root/'control.json').write_text(json.dumps(self.control));git('add','.');git('commit','-qm','frozen origin');self.origin=git('rev-parse','HEAD')
  (self.root/'p0/index.html').write_text('<main>Historical0 plus new reader content.</main>');git('add','.');git('commit','-qm','authorized current addition')
 def find(self):return find_frozen_origin(self.root,'control.json',self.control,Parser,lambda t:' '.join(t.split()))
 def test_origin_verified_without_restoring_current(self):
  origin,surfaces=self.find();self.assertEqual(origin,self.origin);self.assertEqual(len(surfaces),18);self.assertIn('new reader',(self.root/'p0/index.html').read_text())
 def test_uncommitted_control_mutation_fails(self):
  (self.root/'control.json').write_text('{}')
  with self.assertRaises(ValueError):self.find()
 def test_missing_current_route_fails(self):
  (self.root/'p0/index.html').unlink()
  with self.assertRaises(ValueError):self.find()
 def test_broken_historical_hash_fails(self):
  self.control['rendered_occurrence_control']['route_snapshots'][0]['normalized_main_sha256']='0'*64
  (self.root/'control.json').write_text(json.dumps(self.control));self.git('add','.');self.git('commit','-qm','invalid control')
  with self.assertRaises(ValueError):self.find()
if __name__=='__main__':unittest.main()
