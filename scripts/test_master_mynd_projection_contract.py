from pathlib import Path
import re,unittest
from master_mynd_projection_contract import without_master_mynd_discovery,PREFIX
ROOT=Path(__file__).resolve().parents[1]
class ProjectionTests(unittest.TestCase):
 def setUp(self):
  self.path='en/authorities-duties-asset-recovery/index.html'
  self.source=(ROOT/self.path).read_text()
  self.block=re.search(re.escape(PREFIX)+r'.*?</section>\n',self.source,re.S)[0]
 def test_exact_backlink_projection_only(self):
  result=without_master_mynd_discovery(self.source,self.path)
  self.assertEqual(self.source,result.replace('</main>',self.block+'</main>',1))
 def test_changed_claim_fails(self):
  with self.assertRaises(AssertionError):without_master_mynd_discovery(self.source.replace('not a corporate owner','the corporate owner'),self.path)
 def test_duplicate_fails(self):
  with self.assertRaises(AssertionError):without_master_mynd_discovery(self.source.replace(self.block,self.block*2),self.path)
 def test_different_page_fails(self):
  with self.assertRaises(AssertionError):without_master_mynd_discovery(self.source,'en/unregistered/index.html')
 def test_prior_content_not_masked(self):
  changed=self.source.replace('<main','<main data-regression="true"',1)
  self.assertNotEqual(without_master_mynd_discovery(changed,self.path),without_master_mynd_discovery(self.source,self.path))
 def test_nested_or_moved_block_fails(self):
  changed=self.source.replace(self.block,'').replace('</main>',self.block+'<p>Moved boundary</p></main>')
  with self.assertRaises(AssertionError):without_master_mynd_discovery(changed,self.path)
 def test_without_block_is_identical(self):
  source=without_master_mynd_discovery(self.source,self.path)
  self.assertEqual(without_master_mynd_discovery(source,self.path),source)
if __name__=='__main__':unittest.main()
