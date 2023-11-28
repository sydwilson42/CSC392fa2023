var express = require('express');
var router = express.Router();

/* 
 * GET home page.  The function here basically just calls runMainQuery()
 * with a fixed query.
 */
router.get('/', function(req, res, next) {
    req.app.locals.query = "SELECT * from School;";
    runMainQuery(req, res, next);
});


/* 
 * POST home page.  The function here figures out the query to run and
 * calls runMainQuery() with that function.  
 */
router.post('/', function(req, res, next) {
    let query = '';
    if (req.body.CrsID) {
        // Run the equivalence query
        query = `SELECT College, CrsCode, CrsName, CreditHrs, ARCCode `
                + `FROM School natural join Course natural join Equivalence `
                + `WHERE CrsID = ${req.body.CrsID};`
    }
    req.app.locals.query = query;
    runMainQuery(req, res, next)
});

/*
 * Run the main SQL query, if there is one.  Attach the query text and the
 * rows of the result to req.app.locals, so we don't have to pass huge 
 * numbers of parameters to the functions downstream.  If there's no main
 * SQL query, then the query text is just the empty string and the rows are
 * an empty array.  Whether there's a main query or not, finish by calling
 * runSchoolsQuery().
 */
function runMainQuery(req, res, next) {
    if (req.app.locals.query) {
        req.app.locals.db.all(req.app.locals.query, [], (err, rows) => {
            if (err) {
                throw err;
            }
            req.app.locals.rows = rows;
            runSchoolsQuery(req, res, next); // Has to happen in the handler function
        });
    }
    else { // No query
        req.app.locals.rows = [];  // Empty array
        runSchoolsQuery(req, res, next);
    }
}

/*
 * Run the schools query to fill the schools dropdown.  Again, attach the
 * rows of the result (under the name "schools") to req.app.locals.  Finish
 * by calling runCoursesQuery().
 */
function runSchoolsQuery(req, res, next) {
    let schools_query = 'SELECT OrgCode, College from School;';
    req.app.locals.db.all(schools_query, [], (err, schools) => {
        if (err) {
            throw err;
        }
        req.app.locals.schools = schools;
        runCoursesQuery(req, res, next);  // Has to happen in the handler function
    });
}

/*
 * If orgCode is specified in the form data, run the courses query to fill
 * the courses dropdown.  As with the schools query, attach the rows of the
 * query result (under the name "courses") to req.app.locals.  If orgCode is
 * *not* specified, req.app.locals.courses is just an empty array.  Either
 * way, finish by calling showIndex().
 */
function runCoursesQuery(req, res, next) {
    if (!req.body.OrgCode) {  // No school specified, don't run the query
        req.app.locals.courses = [];
        showIndex(req, res, next);
    }
    else {  // req.body.OrgCode is specified
        // FILL IN THE COURSES QUERY AND RUN IT
        let courses_query = `SELECT CrsID, CrsName FROM Course natural join School` + `WHERE OrgCode = ${req.body.OrgCode};`;
        req.app.locals.db.all(courses_query, [], (err, courses) => {
            if (err){
                throw err;
            }
            req.app.locals.courses = courses;
            showIndex(req, res, next); // Eventually needs to be inside the handler function       
        })  
    }
}

/*
 * This function actually renders the HTML page on the result, using
 * index.pug.  Much of what happens in this function is extracting
 * values from req.apps.locals to pass as parameters to index.pug.
 */
function showIndex(req, res, next) {
    res.render('index', { title : 'Equivalence Portal',
                            query: req.app.locals.query,
                            rows: req.app.locals.rows,
                            schools: req.app.locals.schools,
                            OrgCode: req.body.OrgCode,
                            courses: req.app.locals.courses,
                            crsID: req.body.crsID,
                            postdata: req.body });
}


module.exports = router;
