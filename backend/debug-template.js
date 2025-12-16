const Handlebars = require('handlebars');

// Register Handlebars helpers
Handlebars.registerHelper('json', function(context) {
  return JSON.stringify(context, null, 2);
});

Handlebars.registerHelper('ifEquals', function(arg1, arg2, options) {
  return (arg1 == arg2) ? options.fn(this) : options.inverse(this);
});

// Test data that matches what we're sending to the template
const testData = {
  title: "Q4 Compliance Report",
  reportType: "compliance",
  generatedAt: "Mon Dec 15 2025 22:10:55 GMT+0530 (India Standard Time)",
  content: {
    summary: {
      totalRegulations: 142,
      compliant: 128,
      nonCompliant: 5,
      pending: 9
    },
    data: [
      {
        jurisdiction: "United States",
        regulation: "GDPR Compliance Act",
        status: "compliant"
      },
      {
        jurisdiction: "Canada",
        regulation: "PIPEDA Amendment #42",
        status: "non-compliant",
        action: "Update privacy policy by Jan 15, 2026"
      }
    ]
  },
  reportId: "cda59a40-3269-470f-bd26-691ce1e8f3b3"
};

// Test template that should work
const testTemplate = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>{{title}}</title>
</head>
<body>
  <h1>{{title}}</h1>
  <p>Report Type: {{reportType}}</p>
  <p>Generated At: {{generatedAt}}</p>
  
  {{#if content.summary}}
  <h2>Summary</h2>
  <ul>
    <li>Total Regulations: {{content.summary.totalRegulations}}</li>
    <li>Compliant: {{content.summary.compliant}}</li>
    <li>Non-Compliant: {{content.summary.nonCompliant}}</li>
    <li>Pending: {{content.summary.pending}}</li>
  </ul>
  {{/if}}
  
  {{#if content.data}}
  <h2>Detailed Findings</h2>
  <table border="1">
    <thead>
      <tr>
        <th>Jurisdiction</th>
        <th>Regulation</th>
        <th>Status</th>
        <th>Action Required</th>
      </tr>
    </thead>
    <tbody>
      {{#each content.data}}
      <tr>
        <td>{{this.jurisdiction}}</td>
        <td>{{this.regulation}}</td>
        <td>{{this.status}}</td>
        <td>{{this.action}}</td>
      </tr>
      {{/each}}
    </tbody>
  </table>
  {{/if}}
  
  <hr>
  <h3>Debug: Raw Content Object</h3>
  <pre>{{json content}}</pre>
</body>
</html>
`;

try {
  const template = Handlebars.compile(testTemplate);
  const result = template(testData);
  console.log("Template rendered successfully!");
  console.log(result);
} catch (error) {
  console.error("Error rendering template:", error);
}