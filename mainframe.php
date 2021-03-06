<script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
<script type="text/javascript">
    function toggle(input){
        var x = document.getElementById(input);
        if (x.style.display == "none"){
            x.style.display = "block";
            } else {
            x.style.display = "none";
        }
    }
    $(function() {
        $("#custom_checkbox").change(function() {
            $("#CustomGenome").toggle();
        });
    });
</script>

<div style="width:100%; align:center">
    <table style="margin:0 auto;">
        <tr>
            <td>
                <div class="bigblock">
                    <div class="subtitle"> <b>Co</b>mprehensive <b>Re</b>dundancy Analysis for <b>Co</b>mplete <b>P</b>roteomes </div>

                    <div class="general">
                        <form name="download" action="results.php" method="POST" enctype="multipart/form-data">
                            <div id="download_area">
                                <br><b>FASTA: </b> <input type="file" name="fastaseq"><br>
                                <input type='checkbox' name="exfile"> Use Example File? <p>
                                <b>EMAIL (optional): </b> <input type="text" name="email"></input>
                                <p><b>PARAMETERS</b></p>
                                <table>
                                    <tr>
                                        <td>
                                            <table>
                                                <tr>
                                                    <td class="setting_title">
                                                        <b>Sequence Length: </b>
                                                        <a href="javascript:toggle('Length_Description')">(?)</a>
                                                    </td>
                                                    <td>
                                                        <input type="checkbox" name="dlen"> <b>Skip</b>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr id = "Length_Description" style="display: none;width: 20em;">
                                        <td class="descript setting">Flag sequences that are less that <b>m</b> or more than <b>n</b> amino acids long. Check <b>Skip</b> to bypass</td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <table>
                                                <tr>
                                                    <td class="setting">
                                                        Minimum (m):
                                                    </td>
                                                    <td>
                                                        <input type="text" name="min" value="30" class="param"></input>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td class="setting">
                                                        Maximum (n):
                                                    </td>
                                                    <td>
                                                        <input type="text" name="max" value="30000" class="param"></input>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <table>
                                                <tr>
                                                    <td class="setting_title"><b>Intra-Sequence Complexity: </b><a href="javascript:toggle('ISC_Description')">(?)</a></td><td><input type="checkbox" name="dcomp"> <b>Skip</b> </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr id = "ISC_Description" style="display: none;width: 20em;">
                                        <td class="descript setting">Flag sequences compressible at least down to <b>c</b> of the original length (repetitive structure). Check <b>Skip</b> to bypass
                                    </tr>
                                    <tr>
                                        <td>
                                            <table>
                                                <tr>
                                                    <td class="setting">
                                                        Complexity (c):
                                                    </td>
                                                    <td>
                                                        <input type="text" name="zj" value="0.7" class="param"></input>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <table>
                                                <tr>
                                                    <td class="setting_title"><b>Inter-Sequence Redundancy: </b><a href="javascript:toggle('ISR_Description')">(?)</a></td><td> <input type="checkbox" name="dred"> <b>Skip</b> </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr id = 'ISR_Description' style="display: none;width: 20em;">
                                        <td class="descript setting">Flag sequences contained with atleast <b>t</b> sequence identity within up to <b>f</b> fractional length of another sequence in this set. Check <b>Skip</b> to bypass
                                    </tr>
                                    <tr>
                                        <td>
                                            <table>
                                                <tr>
                                                    <td class="setting">
                                                        Identity (t):
                                                    </td>
                                                    <td>
                                                        <input type="text" name="ct" value="0.7" class="param"></input>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td class="setting">
                                                        Fractional Length (f):
                                                    </td>
                                                    <td>
                                                        <input type="text" name="cl" value="0.8" class="param"></input>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
<!--
                                    <tr>
                                        <td>
                                            <table>
                                                <tr>
                                                    <td class="setting_title"><b>Fission: </b><a href="javascript:toggle('FIS_Description')">(?)</a></td><td> <input type="checkbox" name="dfis"> Bypass? </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>

                                    <tr id = 'FIS_Description' style="display: none;width: 20em;">
                                        <td class="descript setting">Flag sequences that are potentially joinable fragments of <b>Reference Genome</b>. Check <b>Skip</b> to bypass
                                    </tr>
                                    <tr>
                                        <td>
                                            <table>
                                                <tr>

                                                    <td class="setting"><i>Reference Genome:</i></td>
                                                </tr>
                                                <tr>
                                                    <td class="setting">
                                                        <input type="checkbox" name="refgm" value="human"> Homo Sapiens
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td class = "setting">
                                                        <input type="checkbox" name="refgm" value="xtrop"> Xenopus Tropicalis
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td class="setting">
                                                        <input type="checkbox" id="custom_checkbox" name="refgm" value="custom"> Custom
                                                    </td>
                                                </tr>
                                                <tr id = 'CustomGenome' style="display:none;">
                                                    <td class="setting">
                                                        <input type="file" name="refgm_file">
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr> -->
                                    <tr>
                                        <td><b>Miscellaneous Settings:</b></td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <table>
                                                <tr>
                                                    <td class="setting">
                                                        "X" tolerance (x):
                                                    </td>
                                                    <td style="width: 80px;">
                                                        <input type="text" name="xs" value="0" class="param"></input>
                                                        <a href="javascript:toggle('XS_Description')">(?)</a>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr id = 'XS_Description' style="display: none;">
                                        <td class="descript setting">Flag sequences with regions containing more than <b>x</b> consecutive "X"s</td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <table>
                                                <tr>
                                                    <td class="setting">
                                                        Check for M at beginning of sequence?
                                                    </td>
                                                    <td class="checkbox_setting">
                                                        <input type="checkbox" name="ms"><a href="javascript:toggle('MS_Description')">(?)</a>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr id = 'MS_Description' style="display: none;">
                                        <td class="descript setting">When checked flag sequences not beggining with "M"</td>
                                    </tr>
                                </table>
                                <div style="height:20px;"></div>
                                
                                <p></p>
                                <input type="submit"/>
                            </div>
                            <p>
                            <div style="font-size:50%;">
                                <b>Contact:</b><i><br>pesha (at) hms.harvard.edu <br> jonathan (at) patsenker.com</i>
                            </div>
                        </form>
                    </div>
                </div>
            </td>
    </table>
</div>