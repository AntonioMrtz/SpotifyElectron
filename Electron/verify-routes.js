/**
 * Route Verification Script
 * Verifies that all playlist routes are consistent after the bug fix
 */

const fs = require('fs');
const path = require('path');

// Files to check for route patterns
const filesToCheck = [
  'src/renderer/App.tsx',
  'src/components/Sidebar/Sidebar.tsx',
  'src/components/AdvancedUIComponents/ContextMenu/Playlist/ContextMenuPlaylist.tsx'
];

function checkRouteConsistency() {
  console.log('🔍 Checking route consistency across files...\n');
  
  let allConsistent = true;
  const routePatterns = [];
  
  filesToCheck.forEach(filePath => {
    const fullPath = path.join(__dirname, filePath);
    
    if (!fs.existsSync(fullPath)) {
      console.log(`⚠️  File not found: ${filePath}`);
      return;
    }
    
    const content = fs.readFileSync(fullPath, 'utf8');
    
    // Look for playlist route patterns
    const playlistRoutes = content.match(/\/playlist[s]?\/[^"'\s]*/g) || [];
    const routeDefinitions = content.match(/path="\/playlist[s]?[^"]*"/g) || [];
    
    console.log(`📁 ${filePath}:`);
    
    if (playlistRoutes.length > 0) {
      playlistRoutes.forEach(route => {
        console.log(`  📍 Route: ${route}`);
        routePatterns.push({ file: filePath, route });
      });
    }
    
    if (routeDefinitions.length > 0) {
      routeDefinitions.forEach(def => {
        console.log(`  🛣️  Definition: ${def}`);
        routePatterns.push({ file: filePath, route: def });
      });
    }
    
    if (playlistRoutes.length === 0 && routeDefinitions.length === 0) {
      console.log(`  ✅ No playlist routes found`);
    }
    
    console.log('');
  });
  
  // Check for consistency
  const frontendRoutes = routePatterns.filter(p => 
    p.route.includes('/playlist/') && !p.route.includes('/playlists/')
  );
  
  const incorrectRoutes = routePatterns.filter(p => 
    p.route.includes('/playlists/') && !p.file.includes('test')
  );
  
  console.log('📊 Analysis:');
  console.log(`  ✅ Correct frontend routes (/playlist/): ${frontendRoutes.length}`);
  console.log(`  ❌ Incorrect frontend routes (/playlists/): ${incorrectRoutes.length}`);
  
  if (incorrectRoutes.length > 0) {
    console.log('\n⚠️  Found incorrect routes:');
    incorrectRoutes.forEach(r => {
      console.log(`    ${r.file}: ${r.route}`);
    });
    allConsistent = false;
  }
  
  console.log(`\n🎯 Route consistency: ${allConsistent ? '✅ PASS' : '❌ FAIL'}`);
  
  return allConsistent;
}

function verifySpecificFix() {
  console.log('🔧 Verifying specific bug fix...\n');
  
  const contextMenuFile = 'src/components/AdvancedUIComponents/ContextMenu/Playlist/ContextMenuPlaylist.tsx';
  const fullPath = path.join(__dirname, contextMenuFile);
  
  if (!fs.existsSync(fullPath)) {
    console.log(`❌ Context menu file not found: ${contextMenuFile}`);
    return false;
  }
  
  const content = fs.readFileSync(fullPath, 'utf8');
  
  // Check for the correct route in handleEditPlaylistData
  const hasCorrectRoute = content.includes('navigate(`/playlist/${playlistName}?edit=true`');
  const hasIncorrectRoute = content.includes('navigate(`/playlists/${playlistName}?edit=true`');
  
  console.log(`📁 ${contextMenuFile}:`);
  console.log(`  ✅ Has correct route (/playlist/): ${hasCorrectRoute}`);
  console.log(`  ❌ Has incorrect route (/playlists/): ${hasIncorrectRoute}`);
  
  const fixApplied = hasCorrectRoute && !hasIncorrectRoute;
  console.log(`\n🎯 Bug fix applied: ${fixApplied ? '✅ PASS' : '❌ FAIL'}`);
  
  return fixApplied;
}

function main() {
  console.log('🚀 Route Verification Script\n');
  console.log('=' .repeat(50));
  
  const consistencyCheck = checkRouteConsistency();
  console.log('=' .repeat(50));
  
  const fixCheck = verifySpecificFix();
  console.log('=' .repeat(50));
  
  const allPassed = consistencyCheck && fixCheck;
  
  console.log('\n📋 Final Results:');
  console.log(`  Route Consistency: ${consistencyCheck ? '✅ PASS' : '❌ FAIL'}`);
  console.log(`  Bug Fix Applied: ${fixCheck ? '✅ PASS' : '❌ FAIL'}`);
  console.log(`  Overall: ${allPassed ? '✅ ALL CHECKS PASSED' : '❌ SOME CHECKS FAILED'}`);
  
  if (allPassed) {
    console.log('\n🎉 The playlist edit bug fix is correctly implemented!');
    console.log('   All routes are consistent and the fix is properly applied.');
  } else {
    console.log('\n⚠️  There are issues that need to be addressed.');
  }
  
  return allPassed;
}

// Run the verification
main();
