$PROJECT = 'diffpy.nmf_mapping'
$ACTIVITIES = ['version_bump', 'changelog', 'tag', 'push_tag', 'ghrelease']

$VERSION_BUMP_PATTERNS = [
    ('diffpy/nmf_mapping/__init__.py', '__version__\s*=.*', "__version__ = '$VERSION'"),
    ('setup.py', 'version\s*=.*,', "version='$VERSION',")
    ]
$CHANGELOG_FILENAME = 'CHANGELOG.rst'
$CHANGELOG_IGNORE = ['TEMPLATE.rst']
$PUSH_TAG_REMOTE = 'git@github.com:diffpy/diffpy.nmf_mapping.git'

$GITHUB_ORG = 'diffpy'
$GITHUB_REPO = 'diffpy.nmf_mapping'
